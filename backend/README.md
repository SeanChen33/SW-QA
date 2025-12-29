# 企业Q&A Agent 后端服务

基于百炼平台的企业Q&A Agent后端服务，支持文档上传、向量数据库训练和流式响应问答。

## 功能特性

- 📄 支持多种文档格式（PDF、Word、Excel、TXT）
- 🔍 基于向量数据库的语义搜索
- 💬 流式响应问答
- 🏢 支持多公司数据隔离
- 🚀 基于FastAPI的高性能API

## 安装依赖

### Windows
```bash
cd backend
install.bat
```

### Linux/Mac
```bash
cd backend
chmod +x install.sh
./install.sh
```

### 手动安装
```bash
cd backend
# 先升级pip和基础工具
python -m pip install --upgrade pip setuptools wheel
# 然后安装依赖
pip install -r requirements.txt
```

**注意**: 如果遇到安装错误，请确保：
1. Python版本 >= 3.8
2. 已安装最新版本的pip、setuptools和wheel
3. 如果使用Python 3.13，某些包可能需要从源码编译，确保已安装C++编译工具

## 配置

1. 复制 `.env.example` 为 `.env`
2. 在 `.env` 中配置百炼平台API Key

```env
DASHSCOPE_API_KEY=sk-16ef02df3d9a4605b096b84c5fe327e5
```

## 运行服务

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动

## API接口

### 1. 上传文档

```bash
POST /api/upload
Content-Type: multipart/form-data

file: [文件]
company_id: default (可选)
```

### 2. 问答接口（流式）

```bash
POST /api/qa
Content-Type: application/json

{
  "question": "你们公司的产品有哪些？",
  "company_id": "default",
  "stream": true
}
```

### 3. 问答接口（非流式）

```bash
POST /api/qa
Content-Type: application/json

{
  "question": "你们公司的产品有哪些？",
  "company_id": "default",
  "stream": false
}
```

### 4. 获取文档列表

```bash
GET /api/documents/{company_id}
```

### 5. 删除文档

```bash
DELETE /api/documents/{company_id}/{file_id}
```

## 使用示例

### Python示例

```python
import requests

# 上传文档
with open("company_doc.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/upload",
        files={"file": f},
        data={"company_id": "company_001"}
    )
print(response.json())

# 流式问答
response = requests.post(
    "http://localhost:8000/api/qa",
    json={
        "question": "公司的主要业务是什么？",
        "company_id": "company_001",
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

### JavaScript示例

```javascript
// 流式问答
const response = await fetch('http://localhost:8000/api/qa', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: '公司的主要业务是什么？',
    company_id: 'company_001',
    stream: true
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  const lines = chunk.split('\n');
  
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = line.slice(6);
      if (data === '[DONE]') break;
      const json = JSON.parse(data);
      console.log(json.content);
    }
  }
}
```

## 技术栈

- **FastAPI**: Web框架
- **ChromaDB**: 向量数据库
- **DashScope**: 百炼平台SDK
- **LangChain**: 文本处理
- **Sentence Transformers**: 文本向量化

## 注意事项

1. **Python版本要求**：建议使用 **Python 3.11 或 3.12**。Python 3.13 可能与 ChromaDB 存在兼容性问题，可能导致段错误（Segmentation Fault）。
2. 首次运行会自动创建向量数据库目录
3. 上传的文件会保存在 `uploads/` 目录
4. 向量数据库存储在 `chroma_db/` 目录

## 已知问题

### Python 3.13 兼容性问题

如果使用 Python 3.13 遇到段错误，建议：
1. 降级到 Python 3.11 或 3.12
2. 或者删除 `chroma_db` 目录后重试
3. 如果问题持续，可以考虑使用其他向量数据库（如 FAISS）

