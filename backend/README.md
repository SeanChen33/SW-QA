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
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，配置必要的参数：

**必需配置：**
- `DASHSCOPE_API_KEY`: 百炼平台API Key（必填）
  - 获取地址：https://dashscope.console.aliyun.com/

**可选配置：**
- `MODEL_NAME`: 模型名称（默认：qwen-turbo）
  - 可选值：qwen-turbo, qwen-plus, qwen-max 等
- `TEMPERATURE`: API调用温度参数（默认：0.7）
- `MAX_TOKENS`: 最大token数（默认：2000）
- `FAISS_DB_PATH`: 向量数据库存储路径（默认：./faiss_db）
- `UPLOAD_DIR`: 文件上传存储路径（默认：./uploads）
- `CHUNK_SIZE`: 文本块大小（默认：1000）
- `CHUNK_OVERLAP`: 文本块重叠大小（默认：200）
- `PORT`: 服务端口号（默认：8000）
- `HOST`: 服务主机地址（默认：0.0.0.0）
- `CORS_ORIGINS`: CORS允许的源地址（默认：*）
  - 多个地址用逗号分隔，例如：`http://localhost:3000,http://localhost:5173`
- `LOG_LEVEL`: 日志级别（默认：INFO）
  - 可选值：DEBUG, INFO, WARNING, ERROR, CRITICAL

**注意**：`.env` 文件包含敏感信息，已被 `.gitignore` 忽略，不会提交到代码仓库。

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
- **FAISS**: 向量数据库
- **DashScope**: 百炼平台SDK
- **LangChain**: 文本处理
- **Sentence Transformers**: 文本向量化

## 注意事项

1. **Python版本要求**：建议使用 **Python 3.8+**
2. **环境变量配置**：首次运行前必须配置 `.env` 文件，特别是 `DASHSCOPE_API_KEY`
3. 首次运行会自动创建向量数据库目录和上传目录
4. 上传的文件会保存在配置的 `UPLOAD_DIR` 目录（默认：`uploads/`）
5. 向量数据库存储在配置的 `FAISS_DB_PATH` 目录（默认：`faiss_db/`）

## 故障排查

1. **API Key未配置错误**：确保 `.env` 文件中已正确配置 `DASHSCOPE_API_KEY`
2. **端口被占用**：修改 `.env` 文件中的 `PORT` 配置，或使用命令行参数指定端口：`python main.py 8001`
3. **CORS错误**：在生产环境中，修改 `.env` 文件中的 `CORS_ORIGINS`，设置为实际的前端地址

