# 企业Q&A Agent

一个基于RAG（检索增强生成）的智能问答系统，支持文档上传和流式问答。

## 项目结构

```
SW-QA/
├── frontend/          # 前端项目（Vue3 + Vite）
│   ├── src/
│   │   ├── views/
│   │   │   └── AppSquare.vue    # Q&A Agent主页面
│   │   ├── components/
│   │   │   └── app-square/      # Q&A相关组件
│   │   ├── composables/
│   │   │   └── useChat.js       # 聊天功能
│   │   └── utils/
│   │       ├── api.js            # API调用
│   │       └── constants.js      # 常量定义
│   └── package.json
├── backend/           # 后端服务（Python + FastAPI）
│   ├── main.py
│   ├── services/
│   │   ├── qa_service.py      # 问答服务
│   │   ├── vector_store.py    # 向量数据库
│   │   └── file_processor.py  # 文件处理
│   └── requirements.txt
└── README.md
```

## 快速开始

### 1. 启动后端服务

```bash
cd backend
pip install -r requirements.txt
python main.py
```

后端服务将在 `http://localhost:8000` 启动

### 2. 启动前端服务

```bash
cd frontend
npm install
npm run dev
```

前端服务将在 `http://localhost:5173` 启动（或根据Vite配置的端口）

## 功能特性

- 📄 **文档上传** - 支持PDF、Word、Excel、TXT格式
- 🔍 **智能检索** - 基于向量数据库的语义检索
- 💬 **流式问答** - 实时流式响应，打字机效果展示
- ⚙️ **文档管理** - 支持文档列表查看和删除
- 🎨 **现代化UI** - 黑色背景，流畅的交互体验

## 使用说明

1. 启动后端和前端服务
2. 在浏览器中打开前端应用
3. 在设置页面上传公司文档（PDF、Word、Excel、TXT）
4. 文档会自动处理并训练向量数据库
5. 在输入框提问，获得基于文档的智能回答
6. 支持流式响应，实时显示答案

## 技术栈

### 前端
- Vue 3
- Vue Router
- Vite
- Axios

### 后端
- FastAPI
- FAISS（向量数据库）
- DashScope（百炼平台SDK）
- PyPDF2, python-docx, openpyxl（文档处理）

## API接口

后端提供以下API：

- `POST /api/upload` - 上传文档
- `POST /api/qa` - 问答接口（支持流式）
- `GET /api/documents/{company_id}` - 获取文档列表
- `DELETE /api/documents/{company_id}/{file_id}` - 删除文档

## 注意事项

1. 确保后端服务已启动，前端才能正常调用API
2. 首次上传文档需要等待向量化处理
3. 建议先上传文档再进行问答，以获得更准确的答案
4. 默认使用 `company_id='default'`，可在设置中修改
