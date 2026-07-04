# 更新日志

## [2026-06-23] 成就详情页 & 图片上传

### ✨ 新增功能
- **成就详情页**：点击成就卡片跳转到独立详情页（路由 `/achievement/:slug`）
- **自动生成 slug**：添加成就时根据标题自动生成英文别名（如"成图大赛" → `cheng-tu-da-sai`）
- **图片上传**：CMS 后台支持上传多张图片、预览、删除
- **图片画廊**：详情页画廊展示 + Lightbox 大图预览
- **数据同步**：所有读写统一经过 API 网关（port 7000）

### 🔧 修复
- **个人信息覆盖问题**：CMS 后台保存个人信息时，未提交的字段不再被覆盖为空
  - 根因：profile.html 有 3 个独立 `<form>` 都 POST 到 `/profile`，旧代码用 `request.form.get("field", "")` 把未提交字段覆盖为空
  - 修复：使用 `if request.form.get("field") is not None` 判断，只覆盖实际提交的字段

### 📁 修改文件
| 文件 | 说明 |
|------|------|
| `admin/app.py` | 新增 slug 生成、图片上传/删除 API |
| `admin/templates/achievements.html` | 新增图片上传/预览/删除界面 |
| `src/views/AchievementDetail.vue` | 新增成就详情页组件 |
| `src/views/Achievements.vue` | 卡片点击跳转详情页 |
| `src/router/index.js` | 新增 `/achievement/:slug` 路由 |
| `src/data/achievements.json` | 数据格式更新（含 slug、图片路径） |

---

## [2026-06-22] 项目初始化 & 三层架构搭建

### ✨ 新增功能
- **Vue 3 + Vite 前端**：个人网站前台（port 8080）
- **Flask CMS 后台**：内容管理系统（port 5000）
- **API 网关**：统一数据读写（port 7000）
- **个人信息管理**：CMS 后台可编辑姓名、简介、头像、联系方式
- **动态更新管理**：CMS 后台可发布/编辑/删除动态
- **成就管理**：CMS 后台可添加/编辑/删除成就
- **数据加密**：SQLite 数据库使用加密存储

### 🏗 架构设计
```
Vue 前台 (8080) ──proxy──→ API 网关 (7000) ──→ JSON 文件 + 加密 SQLite
                                    ↑
Flask CMS (5000) ──── gateway_get/post ────┘
```

### 📁 初始文件
- `package.json`、`vite.config.js` — 前端项目配置
- `admin/app.py` — Flask CMS 后端
- `src/data/profile.json` — 个人信息数据
- `src/data/updates.json` — 动态更新数据
- `src/data/achievements.json` — 成就数据


## 视频播放 + 文件下载功能（2026-06-23）

### 视频播放
- **视频存放**: `src/data/videos/`
- **视频 API**: 网关 `GET /api/videos/<文件名>` — 支持 Range 请求（进度条拖动）
- **前台**: Files.vue 点击 ▶️ 播放弹出视频播放器
- **测试视频**: Sintel 预告片 (test-video.mp4, 4.2MB)

### 文件下载
- **文件存放**: `src/data/files/`
- **文件 API**: 网关 `GET /data/files/<文件名>` — 支持直接下载
- **前台**: Files.vue 点击 ⬇️ 下载按钮自动下载
- **Vite 代理**: `/data` 路径也代理到网关 7000 端口

### 已有文件
| 文件 | 大小 | 说明 |
|------|------|------|
| ubuntu-setup-guide.txt | 868 B | Ubuntu 环境配置指南 |
| vue3-quickstart.md | 635 B | Vue 3 学习笔记 |
| go-tools-readme.md | 315 B | Go 工具集介绍 |
| test-video.mp4 | 4.2 MB | Sintel 预告片（可播放） |
