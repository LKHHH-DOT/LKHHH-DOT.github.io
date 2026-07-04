<template>
  <div class="detail-page">
    <!-- 加载中 -->
    <div class="bento-card loading-state" v-if="loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 未找到 -->
    <div class="bento-card empty-state" v-else-if="!achievement">
      <div class="empty-icon">🔍</div>
      <h3>成就未找到</h3>
      <p>这个成就可能已被删除或链接有误</p>
      <router-link to="/achievements" class="back-link">← 返回成就列表</router-link>
    </div>

    <!-- 成就详情 -->
    <template v-else>
      <!-- 返回导航 -->
      <div class="back-nav animate-in">
        <router-link to="/achievements" class="back-btn">
          <span class="back-icon">←</span>
          <span>返回成就列表</span>
        </router-link>
      </div>

      <!-- 主卡片 -->
      <div class="detail-card animate-in" style="animation-delay: 0.1s">
        <div class="detail-header">
          <div class="detail-icon-wrap">
            <span class="detail-icon">{{ getAchieveIcon(achievement.tags) }}</span>
          </div>
          <div class="detail-info">
            <h1 class="detail-title">{{ achievement.title }}</h1>
            <div class="detail-meta">
              <span class="detail-date">📅 {{ achievement.date }}</span>
              <span class="detail-id">#{{ achievement.id }}</span>
            </div>
            <div class="detail-tags" v-if="achievement.tags && achievement.tags.length">
              <span class="bento-tag" v-for="tag in achievement.tags" :key="tag">{{ tag }}</span>
            </div>
          </div>
        </div>

        <!-- 描述 -->
        <div class="detail-body" v-if="achievement.description">
          <p class="detail-description">{{ achievement.description }}</p>
        </div>

        <!-- 外部链接 -->
        <div class="detail-link-bar" v-if="achievement.link">
          <a :href="achievement.link" target="_blank" rel="noopener" class="external-link-btn">
            <span>🔗 查看外部链接</span>
            <span class="link-arrow">→</span>
          </a>
        </div>
      </div>

      <!-- 图片展示 -->
      <div class="detail-card animate-in" style="animation-delay: 0.2s" v-if="achievement.images && achievement.images.length">
        <h2 class="gallery-title">📸 图片展示</h2>
        <div class="gallery-grid">
          <div
            class="gallery-item"
            v-for="(img, idx) in achievement.images"
            :key="idx"
            @click="openLightbox(idx)"
          >
            <img :src="imageUrl(img)" :alt="achievement.title + ' 图片 ' + (idx + 1)" loading="lazy">
            <div class="gallery-overlay">
              <span>🔍 查看大图</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Lightbox 大图预览 -->
      <div class="lightbox" v-if="lightboxOpen" @click="closeLightbox">
        <div class="lightbox-content" @click.stop>
          <button class="lightbox-close" @click="closeLightbox">✕</button>
          <button class="lightbox-nav lightbox-prev" @click="prevImage" v-if="achievement.images.length > 1">‹</button>
          <img :src="imageUrl(achievement.images[lightboxIndex])" alt="大图预览">
          <button class="lightbox-nav lightbox-next" @click="nextImage" v-if="achievement.images.length > 1">›</button>
          <div class="lightbox-counter">{{ lightboxIndex + 1 }} / {{ achievement.images.length }}</div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  name: 'AchievementDetail',
  data() {
    return {
      achievement: null,
      loading: true,
      lightboxOpen: false,
      lightboxIndex: 0
    }
  },
  mounted() {
    this.fetchAchievement()
  },
  watch: {
    '$route'() {
      this.fetchAchievement()
    }
  },
  methods: {
    async fetchAchievement() {
      this.loading = true
      this.lightboxOpen = false
      const slug = this.$route.params.slug
      try {
        const res = await fetch('/api/achievements')
        if (res.ok) {
          const all = await res.json()
          // 先按 slug 匹配，再按 id 匹配（兼容旧数据）
          this.achievement = all.find(a => a.slug === slug) || all.find(a => String(a.id) === slug)
        }
      } catch (e) {
        console.warn('获取成就详情失败', e)
      } finally {
        this.loading = false
      }
    },
    getAchieveIcon(tags) {
      if (!tags || !tags.length) return '🏅'
      const tag = tags[0]
      const iconMap = {
        '比赛': '🏅', '项目': '💻', '证书': '📜',
        '开源': '🌟', '工作': '💼', '学习': '📚',
        '获奖': '🎖️', '活动': '🎪'
      }
      return iconMap[tag] || '🏅'
    },
    openLightbox(idx) {
      this.lightboxIndex = idx
      this.lightboxOpen = true
      document.body.style.overflow = 'hidden'
    },
    closeLightbox() {
      this.lightboxOpen = false
      document.body.style.overflow = ''
    },
    prevImage() {
      this.lightboxIndex = (this.lightboxIndex - 1 + this.achievement.images.length) % this.achievement.images.length
    },
    nextImage() {
      this.lightboxIndex = (this.lightboxIndex + 1) % this.achievement.images.length
    },
    imageUrl(filename) {
      return '/api/achievements/image/' + filename
    }
  },
  beforeUnmount() {
    document.body.style.overflow = ''
  }
}
</script>

<style scoped>
.detail-page {
  max-width: 800px;
  margin: 0 auto;
  padding-bottom: 40px;
}

/* 返回导航 */
.back-nav {
  margin-bottom: 20px;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--text-muted);
  text-decoration: none !important;
  font-size: 0.95rem;
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  transition: all 0.2s;
}

.back-btn:hover {
  background: var(--bg);
  color: var(--text);
  transform: translateX(-3px);
}

.back-icon {
  font-size: 1.2rem;
}

/* 主卡片 */
.detail-card {
  margin-bottom: 20px;
}

.detail-header {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  margin-bottom: 20px;
}

.detail-icon-wrap {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-md);
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.detail-icon {
  font-size: 2rem;
}

.detail-info {
  flex: 1;
}

.detail-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 8px;
  line-height: 1.3;
}

.detail-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.detail-date {
  font-size: 0.9rem;
  color: var(--text-muted);
}

.detail-id {
  font-size: 0.8rem;
  color: var(--text-muted);
  background: var(--bg);
  padding: 2px 8px;
  border-radius: 4px;
}

.detail-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

/* 描述 */
.detail-body {
  margin-bottom: 20px;
}

.detail-description {
  font-size: 1.1rem;
  line-height: 1.8;
  color: var(--text-secondary);
  white-space: pre-wrap;
}

/* 外部链接按钮 */
.detail-link-bar {
  margin-bottom: 0;
}

.external-link-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #eef2ff;
  color: var(--primary);
  border-radius: var(--radius-md);
  font-weight: 600;
  text-decoration: none !important;
  transition: all 0.2s;
}

.external-link-btn:hover {
  background: var(--primary);
  color: white !important;
  transform: translateX(2px);
}

.link-arrow {
  transition: transform 0.2s;
}

.external-link-btn:hover .link-arrow {
  transform: translateX(4px);
}

/* 图片画廊 */
.gallery-title {
  font-size: 1.3rem;
  margin-bottom: 16px;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.gallery-item {
  position: relative;
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  aspect-ratio: 16 / 10;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s;
}

.gallery-item:hover img {
  transform: scale(1.05);
}

.gallery-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.gallery-item:hover .gallery-overlay {
  opacity: 1;
}

.gallery-overlay span {
  color: white;
  font-size: 0.9rem;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.5);
}

/* Lightbox */
.lightbox {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lightbox-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
}

.lightbox-content img {
  max-width: 100%;
  max-height: 85vh;
  border-radius: 8px;
  display: block;
}

.lightbox-close {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 8px;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.lightbox-close:hover {
  opacity: 1;
}

.lightbox-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.15);
  border: none;
  color: white;
  font-size: 2.5rem;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.lightbox-nav:hover {
  background: rgba(255, 255, 255, 0.3);
}

.lightbox-prev {
  left: -60px;
}

.lightbox-next {
  right: -60px;
}

.lightbox-counter {
  position: absolute;
  bottom: -35px;
  left: 50%;
  transform: translateX(-50%);
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
}

/* 加载状态 */
.loading-state {
  text-align: center;
  padding: 80px 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--bg);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  color: var(--text-muted);
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 16px;
}

.empty-state h3 {
  margin-bottom: 8px;
}

.empty-state p {
  color: var(--text-secondary);
  margin-bottom: 20px;
}

.back-link {
  display: inline-block;
  padding: 8px 20px;
  border-radius: var(--radius-md);
  background: var(--gradient-primary);
  color: white !important;
  font-weight: 600;
  text-decoration: none !important;
  transition: all 0.2s;
}

.back-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

/* 响应式 */
@media (max-width: 640px) {
  .detail-title {
    font-size: 1.4rem;
  }

  .detail-icon-wrap {
    width: 48px;
    height: 48px;
  }

  .detail-icon {
    font-size: 1.5rem;
  }

  .gallery-grid {
    grid-template-columns: 1fr;
  }

  .lightbox-prev {
    left: 10px;
  }

  .lightbox-next {
    right: 10px;
  }
}
</style>
