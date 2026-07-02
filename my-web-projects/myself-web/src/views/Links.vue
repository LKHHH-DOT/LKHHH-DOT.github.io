<template>
  <div class="links-page">
    <div class="page-header animate-in">
      <h1 class="page-title">🌐 友情链接</h1>
      <p class="page-desc">我的朋友们</p>
    </div>

    <div v-if="loading" class="loading-state">加载中...</div>

    <div v-if="!loading" class="links-grid">
      <a
        v-for="(link, index) in links"
        :key="link.id || index"
        :href="link.url"
        target="_blank"
        rel="noopener"
        class="link-card animate-in"
        :class="'animate-in-delay-' + Math.min(index % 4 + 1, 4)"
      >
        <div class="link-avatar">
          {{ link.icon || link.name.charAt(0) }}
        </div>
        <div class="link-info">
          <div class="link-name">{{ link.name }}</div>
          <div class="link-desc" v-if="link.description">{{ link.description }}</div>
          <div class="link-url">{{ link.url.replace(/^https?:\/\//, '') }}</div>
        </div>
        <div class="link-arrow">→</div>
      </a>
    </div>

    <div v-if="!loading && links.length === 0" class="empty-state animate-in animate-in-delay-2">
      <div class="empty-icon">🤝</div>
      <div class="empty-text">还没有友链</div>
      <div class="empty-hint">欢迎交换友链！</div>
    </div>

    <!-- 交换友链 -->
    <div class="exchange-card animate-in animate-in-delay-3">
      <h3>🤝 交换友链</h3>
      <p>如果你想和我交换友链，欢迎通过留言或邮件联系我！</p>
      <div class="exchange-info">
        <div class="info-item">
          <span class="info-label">站点名称</span>
          <span class="info-value">小熙的窝</span>
        </div>
        <div class="info-item">
          <span class="info-label">站点地址</span>
          <span class="info-value">https://lazaxa.cn</span>
        </div>
        <div class="info-item">
          <span class="info-label">站点简介</span>
          <span class="info-value">个人技术博客 & 作品集</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE = '/api'

export default {
  name: 'LinksPage',
  data() {
    return {
      links: [],
      loading: true
    }
  },
  methods: {
    async loadLinks() {
      try {
        const res = await fetch(`${API_BASE}/links`)
        const data = await res.json()
        this.links = Array.isArray(data) ? data : (data.data || [])
      } catch (e) {
        console.error('加载友链失败:', e)
        this.links = []
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    this.loadLinks()
  }
}
</script>

<style scoped>
.links-page {
  padding: 32px 16px;
  max-width: 700px;
  margin: 0 auto;
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

.loading-state {
  text-align: center;
  padding: 40px;
  color: var(--text-muted, #94a3b8);
}

/* 链接网格 */
.links-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 32px;
}

.link-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 18px;
  background: var(--card-bg, #fff);
  border: 1px solid var(--border, #e2e8f0);
  border-radius: 14px;
  text-decoration: none !important;
  transition: all 0.2s ease;
}

.link-card:hover {
  border-color: #4f46e5;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.1);
  transform: translateY(-2px);
}

.link-avatar {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #4f46e5, #818cf8);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  font-weight: 700;
  flex-shrink: 0;
}

.link-info {
  flex: 1;
  min-width: 0;
}

.link-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary, #0f172a);
  margin-bottom: 2px;
}

.link-desc {
  font-size: 0.85rem;
  color: var(--text-secondary, #64748b);
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.link-url {
  font-size: 0.8rem;
  color: var(--text-muted, #94a3b8);
}

.link-arrow {
  font-size: 1.2rem;
  color: var(--text-muted, #94a3b8);
  transition: all 0.2s;
  flex-shrink: 0;
}

.link-card:hover .link-arrow {
  color: #4f46e5;
  transform: translateX(4px);
}

/* 交换友链卡片 */
.exchange-card {
  background: var(--card-bg, #fff);
  border: 1px solid var(--border, #e2e8f0);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.exchange-card h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.exchange-card p {
  font-size: 0.9rem;
  color: var(--text-secondary, #64748b);
  margin-bottom: 16px;
}

.exchange-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item {
  display: flex;
  gap: 12px;
  font-size: 0.9rem;
}

.info-label {
  color: var(--text-muted, #94a3b8);
  min-width: 70px;
  flex-shrink: 0;
}

.info-value {
  color: var(--text-primary, #0f172a);
  font-weight: 500;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 12px;
}

.empty-text {
  font-size: 1.1rem;
  color: var(--text-secondary, #64748b);
  margin-bottom: 4px;
}

.empty-hint {
  font-size: 0.9rem;
  color: var(--text-muted, #94a3b8);
}

/* 动画 */
.animate-in {
  opacity: 0;
  transform: translateY(20px);
  animation: slideUp 0.4s ease forwards;
}

.animate-in-delay-1 { animation-delay: 0.1s; }
.animate-in-delay-2 { animation-delay: 0.2s; }
.animate-in-delay-3 { animation-delay: 0.3s; }
.animate-in-delay-4 { animation-delay: 0.4s; }

@keyframes slideUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
