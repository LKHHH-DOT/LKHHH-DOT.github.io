# 🌐 My Web Projects

个人 Web 项目集合 - 包含个人网站和智能问卷系统

## 📁 项目列表

### 1. Myself Web (个人网站)
- **路径**: `./myself-web/`
- **技术栈**: Vue 3 + Vite
- **功能**: 
  - 🏠 个人主页
  - 📝 博客系统
  - 🖼️ 相册展示
  - 🤖 AI 聊天（开发中）
  - 📊 数据统计
  - 📄 项目展示
  - ✍️ 留言板

### 2. Smart Question System (智能问卷系统)
- **路径**: `./smart-question-system/`
- **技术栈**: React 18 + Vite (前端) + Node.js/Express (后端)
- **功能**:
  - 🤖 AI 智能审核（智谱 AI/DeepSeek/OpenAI）
  - 📝 多题型支持（简答/单选/多选/评分）
  - 🔐 用户认证系统（JWT）
  - 🛡️ 反作弊机制（时长检测/IP 限制）
  - 🤖 AI 自动出题
  - 📊 审核日志
  - 📎 CSV 导出

---

## 🚀 快速启动

### Myself Web
```bash
cd myself-web
npm install
npm run dev
```

### Smart Question System
```bash
cd smart-question-system

# 安装依赖
npm install
cd client && npm install && cd ..

# 配置 AI（可选）
cp server/.env.example server/.env
# 编辑 server/.env 填入你的 API Key

# 启动后端
node server/index.js

# 启动前端（新终端）
cd client && npx vite --port 3000
```

---

## 🔐 安全配置

### Smart Question System - .env 配置示例

```bash
# server/.env

# AI 提供商选择：zhipu, deepseek, openai
AI_PROVIDER=zhipu

# 智谱 AI (默认)
ZHIPU_API_KEY=your_zhipu_api_key_here
ZHIPU_MODEL=glm-4-flash

# DeepSeek (可选)
# DEEPSEEK_API_KEY=your_deepseek_api_key_here
# DEEPSEEK_MODEL=deepseek-chat

# OpenAI (可选)
# OPENAI_API_KEY=your_openai_api_key_here
# OPENAI_BASE_URL=https://api.openai.com/v1
# OPENAI_MODEL=gpt-3.5-turbo

# JWT 密钥（生产环境请修改）
JWT_SECRET=your-super-secret-jwt-key-change-in-production
```

---

## 📦 版本管理

Smart Question System 支持版本管理：
```bash
cd smart-question-system

# 查看版本
node scripts/version.js

# 更新版本
node scripts/version.js patch  # 2.0.0 -> 2.0.1
node scripts/version.js minor  # 2.0.0 -> 2.1.0
node scripts/version.js major  # 2.0.0 -> 3.0.0
```

---

## 📝 开发说明

- 所有敏感信息（API Keys、密码、密钥）已使用占位符替换
- 生产环境部署前请配置 `.env` 文件
- 请勿将 `.env` 文件提交到 Git

---

## 📄 License

MIT License

---

## 👤 Author

小熙 (XiaoXi)
智能制造工程专业
