<template>
  <div class="status-page">
    <div class="page-header animate-in">
      <h1 class="page-title">⏰ 在线状态</h1>
      <p class="page-desc">我的成长时间线</p>
    </div>

    <!-- 当前状态 -->
    <div class="bento-card current-status glass animate-in">
      <div class="status-indicator">
        <span class="status-dot online"></span>
        <span class="status-text">在线活跃中</span>
      </div>
      <div class="status-stats">
        <div class="stat-item">
          <span class="stat-number">{{ totalItems }}</span>
          <span class="stat-label">记录条数</span>
        </div>
      </div>
    </div>

    <!-- 时间线 -->
    <div class="status-timeline animate-in animate-in-delay-1">
      <div
        class="timeline-item"
        v-for="(item, idx) in statusList"
        :key="item.id"
        :style="{ animationDelay: `${0.2 + idx * 0.08}s` }"
      >
        <div class="timeline-dot">{{ item.icon }}</div>
        <div class="timeline-content bento-card">
          <div class="timeline-header">
            <h4 class="timeline-title">{{ item.title }}</h4>
            <span class="timeline-date">{{ item.date }}</span>
          </div>
          <p class="timeline-detail">{{ item.detail }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import statusData from '../data/status.json'

export default {
  name: 'StatusPage',
  data() {
    return {
      statusList: statusData
    }
  },
  computed: {
    totalItems() {
      return this.statusList.length
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

/* 当前状态卡片 */
.current-status {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #94a3b8;
}

.status-dot.online {
  background: #22c55e;
  box-shadow: 0 0 8px rgba(34, 197, 94, 0.5);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 8px rgba(34, 197, 94, 0.3); }
  50% { box-shadow: 0 0 16px rgba(34, 197, 94, 0.6); }
}

.status-text {
  font-size: 1.1rem;
  font-weight: 600;
}

.status-stats {
  display: flex;
  gap: 24px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--primary);
}

.stat-label {
  font-size: 0.8rem;
  color: var(--text-muted);
}

/* 时间线 */
.status-timeline {
  position: relative;
  padding-left: 40px;
}

.status-timeline::before {
  content: '';
  position: absolute;
  left: 20px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--border);
}

.timeline-item {
  position: relative;
  margin-bottom: 20px;
  animation: fadeInUp 0.5s ease forwards;
  opacity: 0;
}

.timeline-dot {
  position: absolute;
  left: -28px;
  top: 20px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--card-bg);
  border: 2px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  z-index: 1;
}

.timeline-content {
  padding: 20px;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 8px;
}

.timeline-title {
  font-size: 1.1rem;
  font-weight: 700;
}

.timeline-date {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.timeline-detail {
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.6;
}

@media (max-width: 600px) {
  .current-status {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  .status-timeline {
    padding-left: 32px;
  }
  .timeline-dot {
    left: -20px;
    width: 28px;
    height: 28px;
    font-size: 0.8rem;
  }
}
</style>
