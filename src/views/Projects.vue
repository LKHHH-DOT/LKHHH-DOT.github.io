<template>
  <div class="projects-page">
    <div class="page-header animate-in">
      <h1 class="page-title">📦 项目作品</h1>
      <p class="page-desc">做过的项目，走过的路</p>
    </div>

    <!-- 系列列表 -->
    <div class="section-block animate-in" v-if="seriesList.length">
      <h2 class="section-title">📚 项目系列</h2>
      <div class="series-grid">
        <div
          class="series-card"
          v-for="series in seriesList"
          :key="series.slug"
          @click="goSeries(series.slug)"
          :style="{ '--series-color': series.color }"
        >
          <div class="series-icon">{{ series.icon }}</div>
          <div class="series-info">
            <h3 class="series-name">{{ series.name }}</h3>
            <p class="series-desc">{{ series.description }}</p>
            <span class="series-count">{{ series.count }} 个项目</span>
          </div>
          <div class="series-arrow">→</div>
        </div>
      </div>
    </div>

    <!-- 独立项目（不属于任何系列） -->
    <div class="section-block animate-in" v-if="standaloneProjects.length">
      <h2 class="section-title">📌 独立项目</h2>
      <div class="projects-grid">
        <div
          class="bento-card project-card"
          v-for="(project, idx) in standaloneProjects"
          :key="project.id"
          :style="{ animationDelay: `${idx * 0.1}s` }"
        >
          <div class="project-header">
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
    </div>

    <!-- 空状态 -->
    <div class="empty-state animate-in" v-if="!seriesList.length && !standaloneProjects.length">
      <h3>✨ 还没有项目</h3>
      <p>项目正在路上，敬请期待～</p>
    </div>
  </div>
</template>

<script>
import projectsData from '../data/projects.json'
import seriesData from '../data/series.json'

export default {
  name: 'ProjectsPage',
  data() {
    return {
      projects: projectsData,
      seriesMap: seriesData
    }
  },
  computed: {
    seriesList() {
      return Object.values(this.seriesMap)
    },
    standaloneProjects() {
      return this.projects.filter(p => !p.series)
    }
  },
  methods: {
    goSeries(slug) {
      this.$router.push(`/series/${slug}`)
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

/* ===== 分区标题 ===== */
.section-block {
  margin-bottom: 36px;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--border);
  color: var(--text);
}

/* ===== 系列卡片 ===== */
.series-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: 1fr;
}

@media (min-width: 640px) {
  .series-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.series-card {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 22px;
  background: var(--card-bg);
  border-radius: var(--radius-md);
  border: 2px solid var(--border);
  border-left: 4px solid var(--series-color, var(--primary));
  cursor: pointer;
  transition: all 0.25s;
}

.series-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
  border-color: var(--series-color, var(--primary));
}

.series-icon {
  font-size: 2.4rem;
  flex-shrink: 0;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg);
  border-radius: 12px;
}

.series-info {
  flex: 1;
  min-width: 0;
}

.series-name {
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 6px;
  color: var(--series-color, var(--primary));
}

.series-desc {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.5;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.series-count {
  font-size: 0.8rem;
  color: var(--text-muted);
  background: var(--bg);
  padding: 3px 10px;
  border-radius: 999px;
}

.series-arrow {
  font-size: 1.4rem;
  color: var(--text-muted);
  flex-shrink: 0;
  transition: transform 0.2s;
}

.series-card:hover .series-arrow {
  transform: translateX(4px);
  color: var(--series-color, var(--primary));
}

/* ===== 项目卡片 ===== */
.projects-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: 1fr;
}

@media (min-width: 640px) {
  .projects-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.project-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.project-header {
  display: flex;
  justify-content: flex-end;
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
  font-size: 1.2rem;
  font-weight: 700;
}

.project-desc {
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.6;
  flex: 1;
}

.project-tech {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

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
