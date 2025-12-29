import dashscope
from dashscope import Generation
from typing import AsyncIterator, Dict, List, Any
import os
import logging
from services.vector_store import VectorStore

logger = logging.getLogger(__name__)


class QAService:
    def __init__(self):
        # 设置百炼平台API Key
        self.api_key = os.getenv("DASHSCOPE_API_KEY", "sk-16ef02df3d9a4605b096b84c5fe327e5")
        dashscope.api_key = self.api_key
        
        # 延迟初始化vector_store，避免启动时的段错误
        self._vector_store = None
        self.model = "qwen-turbo"  # 使用通义千问模型
    
    @property
    def vector_store(self):
        """延迟获取vector_store"""
        if self._vector_store is None:
            self._vector_store = VectorStore()
        return self._vector_store
    
    def _build_prompt(self, question: str, context: List[Dict[str, Any]]) -> str:
        """
        构建提示词，包含检索到的上下文
        """
        if context:
            context_text = "\n\n".join([
                f"文档片段 {i+1}:\n{result['content']}"
                for i, result in enumerate(context)
            ])
            prompt = f"""你是一个专业的企业Q&A助手。请基于以下公司文档内容回答用户的问题。

公司文档内容：
{context_text}

用户问题：{question}

请根据上述文档内容回答问题。如果文档中没有相关信息，请说明无法从提供的文档中找到答案。
回答要准确、专业、简洁。"""
        else:
            # 如果没有文档，使用通用回答
            prompt = f"""你是一个专业的企业Q&A助手。用户提出了以下问题：

{question}

请提供专业、准确的回答。如果问题涉及公司具体信息，请提醒用户先上传相关文档。"""
        
        return prompt
    
    async def get_answer(self, question: str, company_id: str = "default") -> str:
        """
        获取非流式答案
        """
        # 从向量数据库检索相关文档
        context = await self.vector_store.search(
            company_id=company_id,
            query=question,
            n_results=5
        )
        
        # 构建提示词
        prompt = self._build_prompt(question, context)
        
        # 调用百炼平台API
        try:
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            response = Generation.call(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                result_format='message'
            )
            
            if response.status_code == 200:
                if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                    return response.output.choices[0].message.content
                else:
                    raise Exception("API返回格式异常")
            else:
                error_msg = getattr(response, 'message', f'状态码: {response.status_code}')
                raise Exception(f"API调用失败: {error_msg}")
        
        except Exception as e:
            raise Exception(f"生成答案失败: {str(e)}")
    
    async def stream_answer(
        self,
        question: str,
        company_id: str = "default"
    ) -> AsyncIterator[Dict[str, str]]:
        """
        流式生成答案
        """
        logger.info(f"开始流式生成答案: question={question[:50]}..., company_id={company_id}")
        
        # 从向量数据库检索相关文档
        context = await self.vector_store.search(
            company_id=company_id,
            query=question,
            n_results=5
        )
        logger.info(f"检索到 {len(context)} 个相关文档片段")
        
        # 构建提示词
        prompt = self._build_prompt(question, context)
        logger.info(f"提示词长度: {len(prompt)} 字符")
        
        # 调用百炼平台流式API
        try:
            # 使用messages格式（新版本API推荐）
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # 尝试调用流式API
            try:
                # 百炼平台的流式API调用
                responses = Generation.call(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2000,
                    stream=True,
                    result_format='message'  # 使用message格式
                )
                logger.info(f"API调用成功，responses类型: {type(responses)}")
                logger.info(f"responses是否为迭代器: {hasattr(responses, '__iter__')}")
            except Exception as e:
                logger.error(f"API调用失败: {str(e)}", exc_info=True)
                raise
            
            has_content = False
            response_count = 0
            accumulated_content = ""  # 跟踪累积的内容，用于计算增量
            
            # 实时处理流式响应，每个响应立即yield
            # 注意：百炼平台的responses是同步生成器，需要在循环中处理并立即yield
            import asyncio
            
            for response in responses:
                response_count += 1
                
                # 每10个响应记录一次日志，避免日志过多
                if response_count % 10 == 0 or response_count <= 3:
                    logger.info(f"处理第{response_count}个响应")
                
                # 检查响应状态
                status_code = getattr(response, 'status_code', None)
                
                if status_code == 200:
                    # 尝试多种方式提取内容
                    current_content = None
                    
                    # 方式1: output.choices[0].message.content
                    try:
                        if hasattr(response, 'output') and response.output:
                            if hasattr(response.output, 'choices') and len(response.output.choices) > 0:
                                choice = response.output.choices[0]
                                if hasattr(choice, 'message') and choice.message:
                                    if hasattr(choice.message, 'content'):
                                        current_content = choice.message.content
                    except Exception as e:
                        logger.debug(f"方式1失败: {e}")
                    
                    # 方式2: output.text
                    if not current_content:
                        try:
                            if hasattr(response, 'output') and response.output:
                                if hasattr(response.output, 'text'):
                                    current_content = response.output.text
                        except Exception as e:
                            logger.debug(f"方式2失败: {e}")
                    
                    # 方式3: 直接访问response.text
                    if not current_content:
                        try:
                            if hasattr(response, 'text'):
                                current_content = response.text
                        except Exception as e:
                            logger.debug(f"方式3失败: {e}")
                    
                    # 方式4: 尝试将response转换为字典
                    if not current_content:
                        try:
                            if hasattr(response, '__dict__'):
                                response_dict = response.__dict__
                                if 'output' in response_dict:
                                    output = response_dict['output']
                                    if isinstance(output, dict):
                                        if 'choices' in output and len(output['choices']) > 0:
                                            choice = output['choices'][0]
                                            if 'message' in choice and 'content' in choice['message']:
                                                current_content = choice['message']['content']
                        except Exception as e:
                            logger.debug(f"方式4失败: {e}")
                    
                    # 如果提取到内容，计算增量并立即发送
                    if current_content:
                        # 检查是否是累积内容（通常流式API返回累积内容）
                        # 如果新内容包含之前的内容，说明是累积的，需要计算增量
                        if current_content.startswith(accumulated_content):
                            # 这是累积内容，提取增量部分
                            delta = current_content[len(accumulated_content):]
                            if delta:  # 只有当有新增内容时才发送
                                has_content = True
                                accumulated_content = current_content  # 更新累积内容
                                # 立即yield，不等待
                                chunk = {
                                    "type": "content",
                                    "content": delta
                                }
                                if response_count <= 3:
                                    logger.info(f"发送第{response_count}个chunk: {chunk}")
                                yield chunk
                                # 关键：每次yield后立即让出控制权，确保数据能及时发送
                                await asyncio.sleep(0.001)  # 1ms延迟，确保流式传输
                        elif accumulated_content and current_content in accumulated_content:
                            # 新内容已经在累积内容中，跳过（可能是重复）
                            continue
                        else:
                            # 新内容，直接发送（可能是增量格式）
                            has_content = True
                            accumulated_content = current_content
                            # 立即yield，不等待
                            chunk = {
                                "type": "content",
                                "content": current_content
                            }
                            if response_count <= 3:
                                logger.info(f"发送第{response_count}个chunk: {chunk}")
                            yield chunk
                            # 关键：每次yield后立即让出控制权，确保数据能及时发送
                            await asyncio.sleep(0.001)  # 1ms延迟，确保流式传输
                else:
                    # API返回错误
                    error_msg = getattr(response, 'message', f'状态码: {status_code}')
                    error_code = getattr(response, 'code', '')
                    logger.error(f"API返回错误: {error_code} - {error_msg}")
                    yield {
                        "type": "error",
                        "content": f"API错误 ({error_code}): {error_msg}"
                    }
                    break
            
            logger.info(f"流式响应处理完成: 收到{response_count}个响应, has_content={has_content}")
            
            # 如果没有收到任何内容，返回提示
            if not has_content:
                logger.warning("未收到任何内容，返回提示信息")
                yield {
                    "type": "content",
                    "content": "抱歉，未能获取到回答。这可能是因为：\n1. 网络连接问题\n2. API服务暂时不可用\n3. 请稍后重试"
                }
            
            yield {"type": "done", "content": ""}
        
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            logger.error(f"流式生成答案失败: {str(e)}\n{error_detail}")
            yield {
                "type": "error",
                "content": f"生成答案失败: {str(e)}\n\n错误详情:\n{error_detail[:500]}"
            }

