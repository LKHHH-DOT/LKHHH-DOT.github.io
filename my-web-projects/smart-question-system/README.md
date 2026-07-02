# 智能问卷系统 v2.0.0

AI 驱动的智能问卷审核平台，防止乱填乱答。

## 功能特性

- 🤖 **AI 智能审核** - 基于智谱 AI/DeepSeek/OpenAI，从相关性、认真度、充实度三维度评分
- 📝 **多题型支持** - 简答题、单选题、多选题、评分题
- 🔐 **用户系统** - 注册登录，JWT 认证
- 🛡️ **反作弊** - 填写时长检测、同 IP 限制
- 🤖 **AI 自动出题** - 输入主题，AI 生成混合题型问卷
- 📊 **审核日志** - 每条回答的 AI 审核详情
- 📎 **CSV 导出** - 一键导出问卷结果
- 💾 **数据持久化** - 文件存储，重启不丢失

## 快速启动

### 方式一：双击 start.bat
```
双击 start.bat 即可一键启动
```

### 方式二：手动启动
```bash
# 安装依赖
npm install
cd client && npm install && cd ..

# 配置 AI（可选，编辑 server/.env）
cp server/.env.example server/.env
# 编辑 server/.env 填入你的 API Key

# 启动后端（端口 5000）
node server/index.js

# 新终端，启动前端（端口 3000）
cd client && npx vite --port 3000
```

## 访问

- 前端：http://localhost:3000
- 后端 API: http://localhost:5000

## 版本管理
```bash
# 查看版本
node scripts/version.js

# 更新版本号
node scripts/version.js patch  # 2.0.0 -> 2.0.1
node scripts/version.js minor  # 2.0.0 -> 2.1.0
node scripts/version.js major  # 2.0.0 -> 3.0.0
```

## 技术栈

- 前端：React 18 + Vite
- 后端：Node.js + Express
- AI: 智谱 AI (GLM-4-Flash) / DeepSeek / OpenAI
- 存储：JSON 文件

## 项目结构

```
smart-question-system/
├── server/          # 后端
│   ├── index.js     # 入口
│   ├── routes/      # API 路由
│   ├── models/      # 数据模型
│   ├── .env.example # 环境配置示例
│   └── data/        # 数据文件（自动生成）
├── client/          # 前端
│   └── src/         # 源码
├── scripts/         # 工具脚本
├── start.bat        # 一键启动脚本
└── README.md
```

## ⚠️ 安全提示

- 生产环境部署前，请修改 `server/.env` 中的 `JWT_SECRET`
- 不要将 `.env` 文件提交到版本控制
- API Keys 请妥善保管
