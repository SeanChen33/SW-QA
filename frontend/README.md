# wenX Platform 前端

Vue3 + Vite 构建的现代化前端应用

## 安装和运行

```bash
cd frontend
npm install
npm run dev
```

前端服务将在 `http://localhost:3000` 启动

## 项目结构

```
frontend/
├── src/
│   ├── components/      # 组件
│   │   ├── Logo.vue
│   │   └── BlackHoleBackground.vue
│   ├── views/          # 页面
│   │   ├── Home.vue    # 首页
│   │   └── QAAgent.vue # 企业Q&A Agent
│   ├── App.vue         # 根组件
│   ├── main.js         # 入口文件
│   └── style.css       # 全局样式
├── index.html
├── vite.config.js
└── package.json
```

## 功能模块

### 首页 (Home.vue)
- 展示通用领域和IC领域的产品
- 点击"立即体验"按钮可跳转到对应功能页面

### 企业Q&A Agent (QAAgent.vue)
- 文档上传（支持PDF、Word、Excel、TXT）
- 流式问答交互
- 文档管理（查看、删除）

## API对接

前端通过 `http://localhost:8000` 对接后端API，已在 `vite.config.js` 中配置代理。

