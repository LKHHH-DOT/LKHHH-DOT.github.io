# 🏠 小熙的个人主页

> 一个简洁、美观的个人展示网站，托管于 GitHub Pages，域名 **[lazaxa.cn](https://lazaxa.cn)**

---

## 📖 项目介绍

这是我的个人主页，用于展示我的**个人简介、比赛经历、项目作品、技术想法**等内容。全静态 HTML 页面，无需后端服务，部署简单，访问快速。

---

## 🗂️ 项目结构

```
my_new_web/
├── CNAME                     # 自定义域名配置
├── style.css                 # 🎨 公共样式表（所有页面共用）
├── index.html                # 🏠 首页
├── about.html                # 👤 关于我
├── experience.html           # 🏆 比赛经历
├── projects.html             # 🛠️ 项目作品
├── ideas.html                # 💡 技术想法/博客
├── series-pid-control.html   # 📚 系列文章 - PID 控制
├── series-smart-questionnaire.html  # 📚 系列文章 - 智能问卷
├── series-bi.html            # 📚 系列文章 - 仿生智慧（BI）
├── vnc-guide.html            # 🔧 VNC 远程桌面配置指南
└── photo/
    └── competitions/         # 🖼️ 比赛相关图片
```

### 页面说明

| 页面 | 文件 | 说明 |
|------|------|------|
| 🏠 首页 | `index.html` | 个人简介、导航入口 |
| 👤 关于我 | `about.html` | 个人介绍、技能标签 |
| 🏆 比赛经历 | `experience.html` | 参加的各类比赛及获奖 |
| 🛠️ 项目作品 | `projects.html` | 开发的项目展示 |
| 💡 技术想法 | `ideas.html` | 技术思考与分享 |
| 📚 PID 控制 | `series-pid-control.html` | PID 控制系列教程 |
| 📚 智能问卷 | `series-smart-questionnaire.html` | 智能问卷系统说明 |
| 📚 仿生智慧 | `series-bi.html` | 仿生智慧（BI）系列 |
| 🔧 VNC 指南 | `vnc-guide.html` | VNC 远程桌面配置教程 |

---

## 🚀 部署指南

### 方式一：GitHub Pages（推荐）

1. **Fork/Clone 本仓库**
2. 在仓库 **Settings → Pages** 中：
   - Source 选择 `Deploy from a branch`
   - Branch 选择 `main`，目录选 `/ (root)`
3. 等待几分钟，访问 `https://你的用户名.github.io`
4. **自定义域名**（可选）：
   - 在仓库 Settings → Pages 中填写你的域名
   - 在域名 DNS 添加 `CNAME` 记录指向 `你的用户名.github.io`

### 方式二：本地预览

```bash
# 使用 Python 内置服务器
cd my_new_web
python3 -m http.server 8080

# 或使用 Node.js
npx serve .
```

打开浏览器访问 `http://localhost:8080` 即可预览。

---

## ✏️ 如何修改内容

### 修改样式

所有页面的公共样式统一在 `style.css` 中，改一个文件即可影响全站：

```css
/* 例如修改主色调 */
--primary: #667eea;  /* 改为你喜欢的颜色 */
```

### 修改个人信息

所有页面都是纯 HTML 文件，直接用文本编辑器打开修改：

```html
<!-- 例如修改首页标题 -->
<h1>小熙的个人主页</h1>
```

### 添加新页面

1. 新建 `.html` 文件
2. 在文件顶部引用公共样式：`<link rel="stylesheet" href="style.css">`
3. 在其他页面的导航栏中添加链接
4. 提交推送即可

### 添加图片

图片统一存放在 `photo/` 目录下，按类别建子文件夹：

```
photo/
└── competitions/    # 比赛相关图片
    └── xxx.jpg
```

在 HTML 中引用：

```html
<img src="photo/competitions/xxx.jpg" alt="比赛照片">
```

---

## 🛠️ 技术栈

- **HTML5** — 页面结构
- **CSS3** — 样式与动画（渐变色背景、弹性布局、响应式设计）
- **公共样式表** — `style.css` 统一管理全站样式
- **纯静态** — 无需数据库、无需后端，加载飞快

---

## 📦 文件上传说明

如需通过 API 上传文件到本仓库，可使用 GitHub API：

```bash
# 上传文件示例
curl -X PUT "https://api.github.com/repos/用户名/仓库名/contents/文件名" \
  -H "Authorization: Bearer 你的Token" \
  -d '{
    "message": "上传说明",
    "content": "base64编码的文件内容"
  }'
```

---

## 📄 许可证

本项目仅供个人展示使用。

---

## 📬 联系我

- 🌐 网站：[lazaxa.cn](https://lazaxa.cn)
- 📧 邮箱：_（待补充）_

---

> **小熙的个人主页** — 记录成长，分享技术 🚀
