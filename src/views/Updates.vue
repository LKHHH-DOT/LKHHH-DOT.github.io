<template>
  <div class="updates-page">
    <div class="page-header animate-in">
      <h2 class="bento-title" style="border: none; margin-bottom: 0;">
        📝 动态更新
        <span class="update-count" v-if="updates.length">{{ updates.length }} 条</span>
      </h2>
    </div>

    <!-- 时间线 -->
    <div class="timeline" v-if="updates.length">
      <div
        class="timeline-item animate-in"
        v-for="(item, idx) in sortedUpdates"
        :key="item.id"
        :style="{ animationDelay: `${0.1 + idx * 0.1}s` }"
      >
        <div class="timeline-marker">
          <div class="timeline-dot"></div>
        </div>
        <div class="bento-card timeline-card">
          <div class="timeline-date">
            <span class="date-badge">{{ item.date }}</span>
          </div>
          <h3 class="timeline-title">{{ item.title }}</h3>
          <p class="timeline-content">{{ item.content }}</p>
          <div class="timeline-tags" v-if="item.tags && item.tags.length">
            <span class="bento-tag" v-for="tag in item.tags" :key="tag">{{ tag }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div class="bento-card empty-state animate-in" v-else>
      <div class="empty-icon">📝</div>
      <h3>暂无动态</h3>
      <p>编辑 <code>src/data/updates.json</code> 添加你的第一条动态吧！</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UpdatesPage',
  data() {
    return {
      updates: []
    }
  },
  computed: {
    sortedUpdates() {
      return [...this.updates].sort((a, b) => {
        if (a.date !== b.date) return b.date.localeCompare(a.date)
        return b.id - a.id
      })
    }
  },
  mounted() {
    this.fetchUpdates()
  },
  methods: {
    async fetchUpdates() {
      try {
        const res = await fetch('/api/updates')
        if (res.ok) {
          this.updates = await res.json()
        }
      } catch (e) {
        console.warn('获取动态数据失败', e)
      }
    }
  }
}
</script>

<style scoped>
.page-header {
  margin-bottom: 24px;
}

.update-count {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-weight: 400;
  margin-left: 8px;
}

/* ===== 时间线 ===== */
.timeline {
  position: relative;
  padding-left: 42px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 20px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: linear-gradient(180deg, var(--primary), var(--primary-light), transparent);
  border-radius: 2px;
}

.timeline-item {
  position: relative;
  margin-bottom: 28px;
}

/* 时间线标记 */
.timeline-marker {
  position: absolute;
  left: -42px;
  top: 26px;
  width: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.timeline-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--gradient-primary);
  border: 3px solid var(--card-bg);
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
  transition: all 0.3s;
}

.timeline-item:hover .timeline-dot {
  transform: scale(1.3);
  box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.3);
}

/* 时间线卡片 */
.timeline-card {
  margin-bottom: 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.timeline-card:hover {
  transform: translateX(4px);
}

.timeline-date {
  margin-bottom: 8px;
}

.date-badge {
  display: inline-block;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--primary);
  background: #eef2ff;
  padding: 4px 12px;
  border-radius: 6px;
  letter-spacing: 0.02em;
}

.timeline-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.timeline-content {
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.7;
  margin-bottom: 12px;
}

.timeline-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
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

.empty-state h3 {
  margin-bottom: 8px;
}

.empty-state p {
  color: var(--text-secondary);
}

code {
  background: var(--bg);
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
  color: var(--primary);
}
</style>
