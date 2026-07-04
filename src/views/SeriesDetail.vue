<template>
  <div class="series-detail-page">
    <div class="page-header animate-in" v-if="series">
      <a class="back-link" @click="goBack">← 返回项目列表</a>
      <h1 class="page-title">{{ series.icon }} {{ series.name }}</h1>
      <p class="page-desc">{{ series.description }}</p>
    </div>

    <!-- 项目列表 -->
    <div class="projects-list animate-in" v-if="seriesProjects.length">
      <div
        class="bento-card project-card"
        v-for="(project, idx) in seriesProjects"
        :key="project.id"
        :style="{ animationDelay: `${idx * 0.1}s` }"
      >
        <div class="project-header">
          <div class="project-number">#{{ project.series_order }}</div>
          <div class="project-status" :class="project.status">
            {{ project.status === '进行中' ? '🔄' : '✅' }}
            {{ project.status }}
          </div>
        </div>
        <h3 class="project-title">{{ project.title }}</h3>
        <p class="project-desc">{{ project.description }}</p>
        <div class="project-tech">
          <span class="bento-tag skill" v-for="tech in project.tech" :key="tech">{{ tech }}</span>
        </div>

        <!-- 文件下载 -->
        <div class="project-files" v-if="project.files">
          <div class="files-title">📎 相关文件</div>
          <div class="files-list">
            <a
              v-if="project.files.paper"
              :href="project.files.paper"
              download
              class="file-link"
            >
              📄 下载论文全文
            </a>
            <a
              v-if="project.files.images && project.files.images.length"
              v-for="(img, i) in project.files.images"
              :key="i"
              :href="img"
              target="_blank"
              class="file-link"
            >
              🖼️ 查看{{ project.files.images.length > 1 ? `图片 ${i + 1}` : '系统架构图' }}
            </a>
          </div>
        </div>

        <!-- 外部链接 -->
        <div class="project-links" v-if="project.link || project.github">
          <a v-if="project.link" :href="project.link" target="_blank" rel="noopener" class="project-link">
            🔗 在线预览
          </a>
          <a v-if="project.github" :href="project.github" target="_blank" rel="noopener" class="project-link">
            🐙 GitHub
          </a>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div class="empty-state animate-in" v-else>
      <h3>📭 该系列暂无项目</h3>
      <p>项目正在路上，敬请期待～</p>
    </div>
  </div>
</template>

<script>
import projectsData from '../data/projects.json'
import seriesData from '../data/series.json'

export default {
  name: 'SeriesDetailPage',
  data() {
    return {
      projects: projectsData,
      seriesMap: seriesData,
      series: null,
      seriesProjects: []
    }
  },
  created() {
    const slug = this.$route.params.slug
    this.series = this.seriesMap[slug] || null

    if (this.series) {
      this.seriesProjects = this.projects
        .filter(p => p.series === slug)
        .sort((a, b) => (a.series_order || 999) - (b.series_order || 999))
    }
  },
  methods: {
    goBack() {
      this.$router.push('/projects')
    }
  }
}
</script>

<style scoped>
.page-header {
  margin-bottom: 32px;
}

.back-link {
  display: inline-block;
  color: var(--primary);
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  margin-bottom: 12px;
  transition: opacity 0.2s;
}

.back-link:hover {
  opacity: 0.7;
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

/* ===== 项目列表 ===== */
.projects-list {
  display: grid;
  gap: 20px;
  grid-template-columns: 1fr;
}

.project-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-number {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--primary);
  opacity: 0.6;
}

.project-status {
  font-size: 0.8rem;
  padding: 4px 10px;
  border-radius: 999px;
  font-weight: 500;
}

.project-status.进行中 {
  background: #fef3c7;
  color: #92400e;
}

.project-status.已完成 {
  background: #d1fae5;
  color: #065f46;
}

.project-title {
  font-size: 1.3rem;
  font-weight: 700;
}

.project-desc {
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.6;
}

.project-tech {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

/* ===== 文件区域 ===== */
.project-files {
  margin-top: 4px;
  padding: 14px;
  background: var(--bg);
  border-radius: var(--radius-sm);
}

.files-title {
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 10px;
  color: var(--text-secondary);
}

.files-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.file-link {
  font-size: 0.85rem;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: var(--radius-sm);
  background: white;
  border: 1px solid var(--border);
  transition: all 0.2s;
}

.file-link:hover {
  background: var(--primary);
  color: white !important;
  border-color: var(--primary);
}

/* ===== 外部链接 ===== */
.project-links {
  display: flex;
  gap: 12px;
  margin-top: 4px;
}

.project-link {
  font-size: 0.9rem;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: var(--radius-sm);
  background: var(--bg);
  transition: all 0.2s;
}

.project-link:hover {
  background: var(--primary);
  color: white !important;
}

/* ===== 空状态 ===== */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
}

.empty-state h3 {
  font-size: 1.5em;
  margin-bottom: 10px;
  color: var(--primary);
}
</style>
