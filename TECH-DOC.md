# myself_web 个人网站 — 技术文档

## 项目概述

小熙的个人网站项目，基于 Vue 3 + Vite 前端 + Flask CMS 后台。

## 端口说明

| 服务 | 端口 | 说明 |
|------|------|------|
| 🌐 前端网站 | **8080** | Vite 开发服务器，对外暴露 |
| 🔧 CMS 后台 | **5000** | Flask 内容管理系统 |

> ⚠️ **端口约定**：前端统一使用 8080 端口，后台统一使用 5000 端口。
> 其他端口（8082、5001 等）均为临时测试或旧进程残留，不应使用。

## 项目结构

```
~/桌面/myself_web/
├── index.html              # 入口 HTML
├── vite.config.js          # Vite 配置（端口 8080）
├── package.json
├── src/
│   ├── main.js             # Vue 入口
│   ├── App.vue
│   ├── router/
│   │   └── index.js        # 路由配置
│   ├── components/
│   ├── views/
│   └── data/               # JSON 数据文件
│       ├── profile.json    # 个人信息
│       ├── updates.json    # 动态更新
│       └── achievements.json # 成就列表
├── admin/
│   ├── app.py              # Flask CMS 后端（端口 5000）
│   ├── requirements.txt
│   └── templates/          # CMS 页面模板
└── public/
```

## 启动方式

### 前端（开发模式）

```bash
cd ~/桌面/myself_web
npx vite --host 0.0.0.0 --port 8080
```

### CMS 后台

```bash
cd ~/桌面/myself_web/admin
python3 app.py
```

## 数据流

```
用户浏览器 ──8080──→ Vite 开发服务器（前端页面）
用户浏览器 ──5000──→ Flask CMS（管理后台，CRUD 操作）
                    ↓
              JSON 文件（src/data/*.json）
```

CMS 后台通过修改 `src/data/` 下的 JSON 文件来更新前端展示内容，无需数据库。

## 访问地址

- **前端网站**: `http://localhost:8080`
- **CMS 后台**: `http://localhost:5000`

## 注意事项

1. 前端和后台**必须同时运行**才能完整使用
2. 修改 JSON 数据后，前端页面刷新即可看到最新内容
3. 如果端口被占用，先检查旧进程：`ss -tlnp | grep -E '8080|5000'`
4. 生产部署时应使用 `npm run build` 构建静态文件，配合 Nginx 反向代理
