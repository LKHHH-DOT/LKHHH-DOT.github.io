# 小熙的个人主页

这是一个基于 GitHub Pages 构建的现代化个人网站，展示智能制造工程专业学生的成长历程、项目实践和创新思考。

## 🌐 网站结构

| 页面 | 文件 | 描述 |
|------|------|------|
| 🏠 首页 | `index.html` | 个人主页入口，展示导航和简介 |
| 📝 简介 | `about.html` | 个人信息、教育背景、技能专长 |
| 🚀 项目 | `projects.html` | 项目展示与实践成果 |
| 🏆 个人经历 | `experience.html` | 得奖经历 + 动态更新（双标签页） |
| 💡 个人想法 | `ideas.html` | 创新想法与灵感库 |

## 🎨 设计特点

- **现代化设计**：渐变紫色主题，响应式布局
- **移动端友好**：完美适配手机、平板、桌面
- **交互体验**：悬停动画、标签切换、平滑过渡
- **简洁高效**：清晰的信息架构，快速加载

## 🚀 访问地址

**主域名**：[https://lazaxa.cn](https://lazaxa.cn)  
**GitHub Pages**：[https://lkhhh-dot.github.io](https://lkhhh-dot.github.io)

## 📝 使用说明

### 添加项目（projects.html）

在 `projects.html` 中找到项目网格区域，复制以下模板：

```html
<div class="project-card">
    <h3>项目名称</h3>
    <div class="tags">
        <span class="tag">标签 1</span>
        <span class="tag">标签 2</span>
    </div>
    <p>项目描述...</p>
    <div class="status status-ongoing">进行中</div>
</div>
```

状态类型：
- `status-ongoing` - 进行中（黄色）
- `status-completed` - 已完成（绿色）
- `status-planned` - 计划中（蓝色）

### 添加奖项（experience.html）

切换到"得奖经历"标签页，复制以下模板：

```html
<div class="award-card">
    <span class="level">国家级/省级/校级</span>
    <h3>奖项名称</h3>
    <p>获奖时间：202X 年 X 月</p>
    <p>奖项描述...</p>
</div>
```

### 添加动态（experience.html）

切换到"动态更新"标签页，复制以下模板：

```html
<div class="timeline-item">
    <h3>动态标题</h3>
    <div class="date">📅 2026 年 X 月 X 日</div>
    <p>动态内容...</p>
</div>
```

### 添加想法（ideas.html）

在 `ideas.html` 中找到想法库区域，复制以下模板：

```html
<div class="idea-card">
    <span class="category">分类标签</span>
    <h3>想法名称</h3>
    <div class="meta">
        <span>📅 2026-XX-XX</span>
        <span>🔄 版本 v1.0</span>
    </div>
    <p>想法描述...</p>
    <div class="status status-draft">构思中</div>
</div>
```

状态类型：
- `status-draft` - 构思中（黄色）
- `status-developing` - 开发中（蓝色）
- `status-mature` - 成熟方案（绿色）

## 🛠️ 技术栈

- **HTML5** - 语义化结构
- **CSS3** - 渐变、动画、响应式
- **JavaScript** - 标签切换交互
- **GitHub Pages** - 静态网站托管

## 📦 部署

网站通过 GitHub Pages 自动部署：

1. 推送代码到 `main` 分支
2. GitHub Pages 自动构建
3. 访问 `https://lkhhh-dot.github.io`

## 📄 许可证

MIT License

## 👤 作者

**小熙**  
智能制造工程专业  
GitHub: [@LKHHH-DOT](https://github.com/LKHHH-DOT)

---

**最后更新**：2026-07-02  
**版本**：v2.0（重构版）
