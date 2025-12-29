from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import uvicorn
from dotenv import load_dotenv
import json
import logging

# 配置日志
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=getattr(logging, log_level.upper(), logging.INFO))
logger = logging.getLogger(__name__)

from services.vector_store import VectorStore
from services.qa_service import QAService
from services.file_processor import FileProcessor

load_dotenv()

app = FastAPI(title="企业Q&A Agent API")

# CORS配置
cors_origins = os.getenv("CORS_ORIGINS", "*")
if cors_origins == "*":
    allow_origins = ["*"]
else:
    allow_origins = [origin.strip() for origin in cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 延迟初始化服务，避免启动时的段错误
vector_store = None
qa_service = None
file_processor = None

def get_vector_store():
    """延迟获取vector_store"""
    global vector_store
    if vector_store is None:
        vector_store = VectorStore()
    return vector_store

def get_qa_service():
    """延迟获取qa_service"""
    global qa_service
    if qa_service is None:
        qa_service = QAService()
    return qa_service

def get_file_processor():
    """延迟获取file_processor"""
    global file_processor
    if file_processor is None:
        file_processor = FileProcessor()
    return file_processor


class QuestionRequest(BaseModel):
    question: str
    company_id: Optional[str] = "default"
    stream: bool = True


class UploadResponse(BaseModel):
    message: str
    file_id: str
    chunks_count: int


@app.get("/")
async def root():
    return {"message": "企业Q&A Agent API服务运行中"}


@app.post("/api/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    company_id: str = Form("default")
):
    """
    上传公司文档并训练向量数据库
    """
    try:
        logger.info(f"收到文件上传请求: filename={file.filename}, company_id={company_id}, content_type={file.content_type}")
        
        # 保存上传的文件
        base_upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
        upload_dir = os.path.join(base_upload_dir, company_id)
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        logger.info(f"保存文件到: {file_path}")
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        logger.info(f"文件保存成功，大小: {len(content)} 字节")
        
        # 处理文件并提取文本
        logger.info(f"开始处理文件: {file_path}")
        text_chunks = await get_file_processor().process_file(file_path, file.filename)
        logger.info(f"文件处理完成，提取到 {len(text_chunks)} 个文本块")
        
        if not text_chunks:
            raise HTTPException(status_code=400, detail="无法从文件中提取文本内容。请确保文件格式正确且包含可提取的文本。")
        
        # 将文本块添加到向量数据库
        logger.info(f"开始添加到向量数据库...")
        file_id = await get_vector_store().add_documents(
            company_id=company_id,
            documents=text_chunks,
            metadata={"filename": file.filename, "file_path": file_path}
        )
        logger.info(f"向量数据库添加成功，file_id: {file_id}")
        
        return UploadResponse(
            message="文档上传并训练成功",
            file_id=file_id,
            chunks_count=len(text_chunks)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理文件时出错: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"处理文件时出错: {str(e)}")


@app.post("/api/qa")
async def ask_question(request: QuestionRequest):
    """
    问答接口，支持流式响应
    """
    try:
        logger.info(f"收到问答请求: question={request.question[:50]}..., company_id={request.company_id}, stream={request.stream}")
        
        if request.stream:
            # 流式响应
            async def generate():
                try:
                    chunk_count = 0
                    async for chunk in get_qa_service().stream_answer(
                        question=request.question,
                        company_id=request.company_id
                    ):
                        chunk_count += 1
                        if chunk_count == 1:
                            logger.info(f"开始流式响应，第一个chunk: {chunk}")
                        # 立即发送chunk，不缓冲
                        chunk_data = f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
                        yield chunk_data
                        # 关键：每次yield后立即让出控制权，确保数据能及时发送到前端
                        import asyncio
                        await asyncio.sleep(0.001)  # 1ms延迟，确保流式传输
                    logger.info(f"流式响应完成，共{chunk_count}个chunk")
                    yield "data: [DONE]\n\n"
                except Exception as e:
                    logger.error(f"流式响应生成错误: {str(e)}", exc_info=True)
                    error_chunk = {
                        "type": "error",
                        "content": f"流式响应错误: {str(e)}"
                    }
                    yield f"data: {json.dumps(error_chunk, ensure_ascii=False)}\n\n"
            
            return StreamingResponse(
                generate(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache, no-transform",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",  # 禁用Nginx缓冲
                    "Content-Type": "text/event-stream; charset=utf-8",
                }
            )
        else:
            # 非流式响应
            answer = await get_qa_service().get_answer(
                question=request.question,
                company_id=request.company_id
            )
            logger.info(f"非流式响应完成，答案长度: {len(answer)}")
            return {"answer": answer}
    
    except Exception as e:
        logger.error(f"问答处理出错: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"问答处理出错: {str(e)}")


@app.get("/api/documents/{company_id}")
async def get_documents(company_id: str):
    """
    获取指定公司的所有文档列表
    """
    try:
        documents = await get_vector_store().get_documents(company_id)
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文档列表出错: {str(e)}")


@app.delete("/api/documents/{company_id}/{file_id}")
async def delete_document(company_id: str, file_id: str):
    """
    删除指定文档
    """
    try:
        await get_vector_store().delete_document(company_id, file_id)
        return {"message": "文档删除成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除文档出错: {str(e)}")


if __name__ == "__main__":
    import sys
    # 允许通过命令行参数指定端口，否则从环境变量读取，默认8000
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)

