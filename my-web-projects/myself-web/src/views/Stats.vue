<template>
  <div class="stats-page">
    <div class="page-header animate-in">
      <h1 class="page-title">📊 数据统计</h1>
      <p class="page-desc">一些有趣的数据</p>
    </div>

    <div class="bento-grid bento-grid-2">
      <!-- GitHub 统计 -->
      <div class="bento-card animate-in animate-in-delay-1">
        <h3 class="bento-title">🐙 GitHub</h3>
        <div class="stats-content">
          <div class="big-number">
            <span class="number">3</span>
            <span class="unit">个仓库</span>
          </div>
          <div class="stat-row">
            <span>持续建设中...</span>
          </div>
        </div>
      </div>

      <!-- 网站统计 -->
      <div class="bento-card animate-in animate-in-delay-2">
        <h3 class="bento-title">🌐 网站</h3>
        <div class="stats-content">
          <div class="big-number">
            <span class="number">{{ pageCount }}</span>
            <span class="unit">个页面</span>
          </div>
          <div class="stat-row">
            <span>Vue 3 + Vite 构建</span>
          </div>
        </div>
      </div>

      <!-- 技术栈 -->
      <div class="bento-card animate-in animate-in-delay-3">
        <h3 class="bento-title">🛠️ 技术栈</h3>
        <div class="tags-cloud">
          <span class="bento-tag skill">Vue 3</span>
          <span class="bento-tag skill">Python</span>
          <span class="bento-tag skill">Go</span>
          <span class="bento-tag skill">Rust</span>
          <span class="bento-tag skill">Docker</span>
          <span class="bento-tag skill">Linux</span>
        </div>
      </div>

      <!-- 学习进度 -->
      <div class="bento-card animate-in animate-in-delay-4">
        <h3 class="bento-title">📈 学习进度</h3>
        <div class="progress-list">
          <div class="progress-item">
            <div class="progress-label">
              <span>前端开发</span>
              <span>70%</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" style="width: 70%"></div>
            </div>
          </div>
          <div class="progress-item">
            <div class="progress-label">
              <span>后端开发</span>
              <span>60%</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" style="width: 60%"></div>
            </div>
          </div>
          <div class="progress-item">
            <div class="progress-label">
              <span>Linux 运维</span>
              <span>50%</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" style="width: 50%"></div>
            </div>
          </div>
          <div class="progress-item">
            <div class="progress-label">
              <span>AI / 机器学习</span>
              <span>30%</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" style="width: 30%"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatsPage',
  computed: {
    pageCount() {
      // 路由中非重定向的页面数量
      return 12
    }
  }
}
</script>

<style scoped>
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

.stats-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.big-number {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.big-number .number {
  font-size: 2.5rem;
  font-weight: 800;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.big-number .unit {
  font-size: 1rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.stat-row {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* 进度条 */
.progress-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.progress-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.progress-bar {
  height: 8px;
  background: var(--bg);
  border-radius: 999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 999px;
  background: var(--gradient-primary);
  transition: width 1s ease;
}
</style>
