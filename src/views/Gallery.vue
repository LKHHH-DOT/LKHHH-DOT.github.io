<template>
  <div class="gallery-page">
    <div class="page-header animate-in">
      <h1 class="page-title">🖼️ 相册</h1>
      <p class="page-desc">记录生活中的美好瞬间</p>
    </div>

    <div v-if="loading" class="loading-state">加载中...</div>

    <!-- 相册分类 -->
    <div v-if="!loading && albums.length > 0" class="albums-section">
      <div
        v-for="(album, aIndex) in albums"
        :key="album.id || aIndex"
        class="album-card animate-in"
        :class="'animate-in-delay-' + Math.min(aIndex % 4 + 1, 4)"
      >
        <div class="album-header">
          <div class="album-info">
            <h3 class="album-title">{{ album.title }}</h3>
            <p class="album-desc" v-if="album.description">{{ album.description }}</p>
            <span class="album-count">{{ album.images.length }} 张</span>
          </div>
          <button
            v-if="album.images.length > 0"
            class="album-toggle"
            @click="toggleAlbum(aIndex)"
          >
            {{ expandedAlbums[aIndex] ? '收起' : '展开' }}
          </button>
        </div>

        <div v-if="expandedAlbums[aIndex]" class="album-images">
          <div
            v-for="(img, iIndex) in album.images"
            :key="iIndex"
            class="gallery-item"
            @click="openLightbox(album.images, iIndex)"
          >
            <img :src="img.url" :alt="img.title || img.caption || ''" loading="lazy" />
            <div class="gallery-overlay">
              <span v-if="img.title">{{ img.title }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!loading && albums.length === 0" class="empty-state animate-in animate-in-delay-2">
      <div class="empty-icon">📸</div>
      <div class="empty-text">相册还是空的</div>
      <div class="empty-hint">期待添加一些照片吧！</div>
    </div>

    <!-- Lightbox -->
    <div v-if="lightboxOpen" class="lightbox" @click.self="closeLightbox">
      <button class="lightbox-close" @click="closeLightbox">✕</button>
      <button class="lightbox-prev" @click="prevImage" v-if="lightboxImages.length > 1">‹</button>
      <div class="lightbox-content">
        <img :src="currentImage.url" :alt="currentImage.title || ''" />
        <div class="lightbox-caption" v-if="currentImage.title || currentImage.caption">
          <div class="caption-title" v-if="currentImage.title">{{ currentImage.title }}</div>
          <div class="caption-text" v-if="currentImage.caption">{{ currentImage.caption }}</div>
        </div>
      </div>
      <button class="lightbox-next" @click="nextImage" v-if="lightboxImages.length > 1">›</button>
      <div class="lightbox-counter" v-if="lightboxImages.length > 1">
        {{ lightboxIndex + 1 }} / {{ lightboxImages.length }}
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE = '/api'

export default {
  name: 'GalleryPage',
  data() {
    return {
      albums: [],
      loading: true,
      expandedAlbums: {},
      lightboxOpen: false,
      lightboxImages: [],
      lightboxIndex: 0
    }
  },
  computed: {
    currentImage() {
      return this.lightboxImages[this.lightboxIndex] || {}
    }
  },
  methods: {
    async loadAlbums() {
      try {
        const res = await fetch(`${API_BASE}/gallery`)
        const data = await res.json()
        this.albums = Array.isArray(data) ? data : (data.data || [])
        // 默认展开第一个相册
        if (this.albums.length > 0) {
          this.$set(this.expandedAlbums, 0, true)
        }
      } catch (e) {
        console.error('加载相册失败:', e)
        this.albums = []
      } finally {
        this.loading = false
      }
    },
    toggleAlbum(index) {
      this.$set(this.expandedAlbums, index, !this.expandedAlbums[index])
    },
    openLightbox(images, index) {
      this.lightboxImages = images
      this.lightboxIndex = index
      this.lightboxOpen = true
      document.body.style.overflow = 'hidden'
    },
    closeLightbox() {
      this.lightboxOpen = false
      document.body.style.overflow = ''
    },
    prevImage() {
      this.lightboxIndex = (this.lightboxIndex - 1 + this.lightboxImages.length) % this.lightboxImages.length
    },
    nextImage() {
      this.lightboxIndex = (this.lightboxIndex + 1) % this.lightboxImages.length
    },
    handleKeydown(e) {
      if (!this.lightboxOpen) return
      if (e.key === 'Escape') this.closeLightbox()
      if (e.key === 'ArrowLeft') this.prevImage()
      if (e.key === 'ArrowRight') this.nextImage()
    }
  },
  mounted() {
    this.loadAlbums()
    window.addEventListener('keydown', this.handleKeydown)
  },
  beforeUnmount() {
    window.removeEventListener('keydown', this.handleKeydown)
    document.body.style.overflow = ''
  }
}
</script>

<style scoped>
.gallery-page {
  padding: 32px 16px;
  max-width: 800px;
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

/* 相册卡片 */
.albums-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.album-card {
  background: var(--card-bg, #fff);
  border: 1px solid var(--border, #e2e8f0);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.album-header {
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.album-info {
  flex: 1;
}

.album-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 4px;
}

.album-desc {
  font-size: 0.85rem;
  color: var(--text-secondary, #64748b);
  margin-bottom: 4px;
}

.album-count {
  font-size: 0.8rem;
  color: var(--text-muted, #94a3b8);
}

.album-toggle {
  padding: 6px 14px;
  border: 1px solid var(--border, #e2e8f0);
  border-radius: 8px;
  background: var(--bg, #f8fafc);
  color: var(--text-secondary, #64748b);
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.album-toggle:hover {
  border-color: #4f46e5;
  color: #4f46e5;
}

/* 图片网格 */
.album-images {
  padding: 0 20px 20px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 10px;
}

.gallery-item {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  aspect-ratio: 1;
  background: var(--bg, #f1f5f9);
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.gallery-item:hover img {
  transform: scale(1.05);
}

.gallery-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 8px 10px;
  background: linear-gradient(transparent, rgba(0,0,0,0.6));
  color: white;
  font-size: 0.8rem;
  opacity: 0;
  transition: opacity 0.2s;
}

.gallery-item:hover .gallery-overlay {
  opacity: 1;
}

/* Lightbox */
.lightbox {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.lightbox-close {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(255,255,255,0.1);
  border: none;
  color: white;
  font-size: 1.5rem;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.lightbox-close:hover {
  background: rgba(255,255,255,0.2);
}

.lightbox-prev,
.lightbox-next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255,255,255,0.1);
  border: none;
  color: white;
  font-size: 2rem;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.lightbox-prev { left: 20px; }
.lightbox-next { right: 20px; }

.lightbox-prev:hover,
.lightbox-next:hover {
  background: rgba(255,255,255,0.2);
}

.lightbox-content {
  max-width: 85vw;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.lightbox-content img {
  max-width: 100%;
  max-height: 75vh;
  object-fit: contain;
  border-radius: 8px;
}

.lightbox-caption {
  margin-top: 12px;
  text-align: center;
  color: white;
}

.caption-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 4px;
}

.caption-text {
  font-size: 0.9rem;
  opacity: 0.8;
}

.lightbox-counter {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  font-size: 0.9rem;
  opacity: 0.7;
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

@media (max-width: 600px) {
  .album-images {
    grid-template-columns: repeat(2, 1fr);
  }
  .lightbox-prev { left: 10px; }
  .lightbox-next { right: 10px; }
}
</style>
