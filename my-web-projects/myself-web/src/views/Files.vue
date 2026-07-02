<template>
  <div class="files-page">
    <div class="page-header animate-in">
      <h1 class="page-title">📁 文件分享</h1>
      <p class="page-desc">分享一些有用的资源</p>
    </div>

    <div class="files-list">
      <div
        class="bento-card file-card animate-in"
        v-for="(file, idx) in files"
        :key="file.id"
        :style="{ animationDelay: `${idx * 0.1}s` }"
      >
        <div class="file-icon">
          <span v-if="file.type === 'pdf'">📄</span>
          <span v-else-if="file.type === 'md'">📝</span>
          <span v-else-if="file.type === 'zip'">📦</span>
          <span v-else-if="file.type === 'video'">🎬</span>
          <span v-else>📎</span>
        </div>
        <div class="file-info">
          <h3 class="file-name">{{ file.name }}</h3>
          <p class="file-desc">{{ file.description }}</p>
          <div class="file-meta">
            <span class="file-type">{{ file.type.toUpperCase() }}</span>
            <span class="file-size">{{ file.size }}</span>
          </div>
        </div>
        <div class="file-action">
          <!-- 视频文件：播放按钮 -->
          <button v-if="file.type === 'video' && file.url"
                  class="download-btn"
                  @click="playVideo(file)">
            ▶️ 播放
          </button>
          <!-- 外部链接下载 -->
          <a v-else-if="file.url && file.url.startsWith('http')"
             :href="file.url"
             class="download-btn"
             target="_blank"
             rel="noopener">
            ⬇️ 下载
          </a>
          <!-- 本地文件下载 -->
          <a v-else-if="file.url && !file.url.startsWith('http')"
             :href="'/data/files/' + file.url"
             class="download-btn"
             download>
            ⬇️ 下载
          </a>
          <!-- 无下载链接 -->
          <span v-else class="coming-soon">即将上线</span>
        </div>
      </div>
    </div>

    <!-- 视频播放弹窗 -->
    <div v-if="showPlayer" class="video-overlay" @click.self="closePlayer">
      <div class="video-modal">
        <div class="video-header">
          <h3>{{ currentVideo.name }}</h3>
          <button class="close-btn" @click="closePlayer">✕</button>
        </div>
        <div class="video-container">
          <video
            ref="videoPlayer"
            :src="currentVideoSrc"
            controls
            autoplay
            class="video-element"
            preload="metadata"
          >
            您的浏览器不支持视频播放
          </video>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import filesData from '../data/files.json'

export default {
  name: 'FilesPage',
  data() {
    return {
      files: Array.isArray(filesData) ? filesData : (filesData.files || []),
      showPlayer: false,
      currentVideo: {}
    }
  },
  computed: {
    currentVideoSrc() {
      if (!this.currentVideo.url) return ''
      // 视频文件通过网关的 /api/videos/ 路径提供
      return `/api/videos/${this.currentVideo.url}`
    }
  },
  methods: {
    playVideo(file) {
      this.currentVideo = file
      this.showPlayer = true
      // 等 DOM 更新后播放
      this.$nextTick(() => {
        const video = this.$refs.videoPlayer
        if (video) {
          video.load()
          video.play().catch(() => {})
        }
      })
    },
    closePlayer() {
      const video = this.$refs.videoPlayer
      if (video) {
        video.pause()
        video.src = ''
      }
      this.showPlayer = false
      this.currentVideo = {}
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

.files-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.file-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px 24px;
}

.file-icon {
  font-size: 2rem;
  flex-shrink: 0;
  width: 48px;
  text-align: center;
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-size: 1.05rem;
  font-weight: 700;
  margin-bottom: 4px;
}

.file-desc {
  color: var(--text-secondary);
  font-size: 0.85rem;
  margin-bottom: 8px;
  line-height: 1.5;
}

.file-meta {
  display: flex;
  gap: 10px;
  font-size: 0.8rem;
}

.file-type {
  padding: 2px 8px;
  border-radius: 4px;
  background: var(--bg);
  color: var(--text-secondary);
  font-weight: 600;
}

.file-size {
  color: var(--text-muted);
}

.file-action {
  flex-shrink: 0;
}

.download-btn {
  display: inline-block;
  padding: 8px 16px;
  background: var(--gradient-primary);
  color: white !important;
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  border: none;
}

.download-btn:hover {
  opacity: 0.9;
  transform: scale(1.05);
}

.coming-soon {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-style: italic;
}

/* 视频播放弹窗 */
.video-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.video-modal {
  background: #1a1a1a;
  border-radius: 12px;
  width: 90%;
  max-width: 900px;
  overflow: hidden;
}

.video-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  color: white;
}

.video-header h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.3rem;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.2s;
}

.close-btn:hover {
  background: rgba(255,255,255,0.1);
}

.video-container {
  width: 100%;
  background: #000;
}

.video-element {
  width: 100%;
  max-height: 70vh;
  display: block;
}

@media (max-width: 600px) {
  .file-card {
    flex-direction: column;
    text-align: center;
  }
  .file-meta {
    justify-content: center;
  }
  .video-modal {
    width: 100%;
    border-radius: 0;
  }
}
</style>
