<template>
  <div class="ai-chat-page">
    <div class="bento-card animate-in">
      <h2 class="bento-title">🤖 AI 对话</h2>
      <p class="text-muted">AI 对话功能正在开发中，敬请期待～</p>
      <div class="coming-soon">
        <span class="coming-soon-icon">🚧</span>
        <span>开发中</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIChat'
}
</script>

<style scoped>
.ai-chat-page {
  max-width: 600px;
  margin: 0 auto;
}
.text-muted {
  color: var(--text-muted);
  margin-top: 8px;
}
.coming-soon {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 24px;
  padding: 12px 20px;
  background: var(--bg);
  border-radius: var(--radius-md);
  font-size: 0.9rem;
  color: var(--text-secondary);
}
.coming-soon-icon {
  font-size: 1.2rem;
}
</style>
