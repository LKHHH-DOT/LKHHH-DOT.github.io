<template>
  <div class="vnc-page">
    <div class="page-header animate-in">
      <h1 class="page-title">🖥️ VNC 远程桌面配置指南</h1>
      <p class="page-desc">Ubuntu 22.04 + x11vnc + Tailscale 完整教程</p>
    </div>

    <div class="md-content animate-in" v-html="renderedContent"></div>

    <div class="back-link animate-in">
      <router-link to="/files" class="back-btn">← 返回文件分享</router-link>
    </div>
  </div>
</template>

<script>
import mdContent from '../data/files/vnc-linux-setup.md?raw'

function renderMarkdown(text) {
  let html = text
    // 标题
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    // 代码块
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>')
    // 行内代码
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // 加粗
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    // 列表
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>')
    // 分割线
    .replace(/^---$/gm, '<hr>')
    // 段落（空行分割）
    .replace(/\n\n/g, '</p><p>')
    // 换行
    .replace(/\n/g, '<br>')

  return '<p>' + html + '</p>'
}

export default {
  name: 'VncGuide',
  data() {
    return {
      renderedContent: renderMarkdown(mdContent)
    }
  }
}
</script>

<style scoped>
.vnc-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 8px;
}

.page-desc {
  color: var(--text-secondary);
  font-size: 1rem;
}

.md-content {
  background: var(--card-bg, #fff);
  border-radius: 16px;
  padding: 24px 32px;
  line-height: 1.8;
  font-size: 0.95rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.md-content :deep(h2) {
  font-size: 1.4rem;
  margin-top: 28px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-color, #eee);
}

.md-content :deep(h3) {
  font-size: 1.15rem;
  margin-top: 20px;
  margin-bottom: 8px;
}

.md-content :deep(p) {
  margin-bottom: 12px;
}

.md-content :deep(code) {
  background: var(--code-bg, #f4f4f5);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.9em;
}

.md-content :deep(pre) {
  background: var(--code-bg, #1e1e2e);
  color: #cdd6f4;
  padding: 16px;
  border-radius: 10px;
  overflow-x: auto;
  font-size: 0.85rem;
  line-height: 1.5;
  margin: 12px 0;
}

.md-content :deep(ul) {
  padding-left: 20px;
  margin-bottom: 12px;
}

.md-content :deep(li) {
  margin-bottom: 4px;
}

.md-content :deep(hr) {
  margin: 20px 0;
  border: none;
  border-top: 1px solid var(--border-color, #eee);
}

.back-link {
  text-align: center;
  margin-top: 32px;
}

.back-btn {
  display: inline-block;
  padding: 10px 24px;
  background: var(--primary, #6366f1);
  color: #fff;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: opacity 0.2s;
}

.back-btn:hover {
  opacity: 0.85;
}
</style>
