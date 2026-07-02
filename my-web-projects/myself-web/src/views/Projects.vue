<template>
  <div class="projects-page">
    <div class="page-header animate-in">
      <h1 class="page-title">📦 项目作品</h1>
      <p class="page-desc">做过的项目，走过的路</p>
    </div>

    <div class="projects-grid">
      <div
        class="bento-card project-card animate-in"
        v-for="(project, idx) in projects"
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
</template>

<script>
import projectsData from '../data/projects.json'

export default {
  name: 'ProjectsPage',
  data() {
    return {
      projects: projectsData
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
</style>
