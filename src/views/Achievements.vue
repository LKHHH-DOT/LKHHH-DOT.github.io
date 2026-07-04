<template>
  <div class="achievements-page">
    <div class="page-header animate-in">
      <h2 class="bento-title" style="border: none; margin-bottom: 0;">
        🏆 重要成就
        <span class="achieve-count" v-if="achievements.length">{{ achievements.length }} 项</span>
      </h2>
    </div>

    <!-- 成就列表 - Bento 卡片 -->
    <div class="achievements-list" v-if="achievements.length">
      <div
        class="bento-card achieve-card animate-in"
        v-for="(item, idx) in sortedAchievements"
        :key="item.id"
        :style="{ animationDelay: `${0.1 + idx * 0.08}s` }"
        @click="goToDetail(item)"
      >
        <div class="achieve-header">
          <div class="achieve-icon-wrap">
            <span class="achieve-icon">{{ getAchieveIcon(item.tags) }}</span>
          </div>
          <div class="achieve-info">
            <h3 class="achieve-title">{{ item.title }}</h3>
            <div class="achieve-meta">
              <span class="achieve-date">{{ item.date }}</span>
              <span class="achieve-id">#{{ item.id }}</span>
            </div>
          </div>
        </div>
        <p class="achieve-desc" v-if="item.description">{{ item.description }}</p>
        <div class="achieve-footer">
          <div class="achieve-tags" v-if="item.tags && item.tags.length">
            <span class="bento-tag" v-for="tag in item.tags" :key="tag">{{ tag }}</span>
          </div>
          <router-link v-if="item.slug" :to="'/achievement/' + item.slug" class="achieve-link">
            <span>📖 查看详情</span>
            <span class="link-arrow">→</span>
          </router-link>
          <a v-else-if="item.link" :href="item.link" target="_blank" rel="noopener" class="achieve-link">
            <span>🔗 外部链接</span>
            <span class="link-arrow">→</span>
          </a>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div class="bento-card empty-state animate-in" v-else>
      <div class="empty-icon">🏆</div>
      <h3>内容筹备中</h3>
      <p>这里将展示你的重要项目和成果，敬请期待！</p>
      <router-link to="/updates" class="empty-link">看看动态 →</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AchievementsPage',
  data() {
    return {
      achievements: []
    }
  },
  computed: {
    sortedAchievements() {
      return [...this.achievements].sort((a, b) => {
        if (a.date !== b.date) return b.date.localeCompare(a.date)
        return b.id - a.id
      })
    }
  },
  mounted() {
    this.fetchAchievements()
  },
  methods: {
    async fetchAchievements() {
      try {
        const res = await fetch('/api/achievements')
        if (res.ok) {
          this.achievements = await res.json()
        }
      } catch (e) {
        console.warn('获取成就数据失败', e)
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
    goToDetail(item) {
      if (item.slug) {
        this.$router.push('/achievement/' + item.slug)
      }
    }
  }
}
</script>

<style scoped>
.page-header {
  margin-bottom: 24px;
}

.achieve-count {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-weight: 400;
  margin-left: 8px;
}

.achievements-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.achieve-card {
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.25s ease;
}

.achieve-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.achieve-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: var(--gradient-primary);
  border-radius: 0 2px 2px 0;
}

.achieve-header {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 12px;
}

.achieve-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.achieve-icon {
  font-size: 1.5rem;
}

.achieve-info {
  flex: 1;
}

.achieve-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 6px;
}

.achieve-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.achieve-date {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.achieve-id {
  font-size: 0.8rem;
  color: var(--text-muted);
  background: var(--bg);
  padding: 2px 8px;
  border-radius: 4px;
}

.achieve-desc {
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.7;
  margin-bottom: 14px;
}

.achieve-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.achieve-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.achieve-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--primary);
  font-size: 0.9rem;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: var(--radius-sm);
  background: #eef2ff;
  transition: all 0.2s;
  text-decoration: none !important;
}

.achieve-link:hover {
  background: var(--primary);
  color: white !important;
  transform: translateX(2px);
}

.link-arrow {
  transition: transform 0.2s;
}

.achieve-link:hover .link-arrow {
  transform: translateX(3px);
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 8px;
}

.empty-state p {
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.empty-link {
  display: inline-block;
  padding: 8px 20px;
  border-radius: var(--radius-md);
  background: var(--gradient-primary);
  color: white !important;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.empty-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}
</style>
