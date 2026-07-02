<template>
  <div class="search-page">
    <div class="page-header animate-in">
      <h1 class="page-title">🔍 全站搜索</h1>
      <p class="page-desc">搜索博客、项目、文件等内容</p>
    </div>

    <div class="search-box animate-in animate-in-delay-1">
      <div class="search-input-wrapper">
        <span class="search-icon">🔍</span>
        <input
          ref="searchInput"
          v-model="query"
          type="text"
          placeholder="输入关键词搜索..."
          class="search-input"
          @input="doSearch"
        />
        <button v-if="query" class="search-clear" @click="clearSearch">✕</button>
      </div>
    </div>

    <div v-if="query && searching" class="searching-indicator animate-in">
      <span>搜索中...</span>
    </div>

    <div v-if="query && !searching" class="search-results">
      <!-- 搜索结果统计 -->
      <div class="result-stats animate-in animate-in-delay-1">
        共找到 <strong>{{ totalResults }}</strong> 条结果
        <span v-if="query">（关键词：<strong>{{ query }}</strong>）</span>
      </div>

      <!-- 博客结果 -->
      <div v-if="blogResults.length > 0" class="result-section animate-in animate-in-delay-2">
        <h3 class="section-title">📖 博客 <span class="result-count">{{ blogResults.length }}</span></h3>
        <div class="result-list">
          <router-link
            v-for="item in blogResults"
            :key="'blog-' + item.id"
            :to="'/blog/' + item.slug"
            class="result-card"
          >
            <div class="result-title">{{ highlightMatch(item.title) }}</div>
            <div class="result-excerpt">{{ highlightMatch(item.summary) }}</div>
            <div class="result-meta">
              <span>{{ item.date }}</span>
              <span v-for="tag in item.tags" :key="tag" class="result-tag">{{ tag }}</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- 项目结果 -->
      <div v-if="projectResults.length > 0" class="result-section animate-in animate-in-delay-3">
        <h3 class="section-title">📦 项目 <span class="result-count">{{ projectResults.length }}</span></h3>
        <div class="result-list">
          <router-link
            v-for="item in projectResults"
            :key="'proj-' + item.id"
            :to="'/projects'"
            class="result-card"
          >
            <div class="result-title">{{ highlightMatch(item.title) }}</div>
            <div class="result-excerpt">{{ highlightMatch(item.description) }}</div>
            <div class="result-meta">
              <span class="result-status" :class="item.status">{{ item.status }}</span>
              <span v-for="t in item.tech" :key="t" class="result-tag">{{ t }}</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- 文件结果 -->
      <div v-if="fileResults.length > 0" class="result-section animate-in animate-in-delay-4">
        <h3 class="section-title">📁 文件 <span class="result-count">{{ fileResults.length }}</span></h3>
        <div class="result-list">
          <router-link
            v-for="item in fileResults"
            :key="'file-' + item.id"
            :to="'/files'"
            class="result-card"
          >
            <div class="result-title">{{ highlightMatch(item.name) }}</div>
            <div class="result-excerpt" v-if="item.description">{{ highlightMatch(item.description) }}</div>
            <div class="result-meta">
              <span>{{ item.type }}</span>
              <span v-if="item.size">{{ item.size }}</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- 动态结果 -->
      <div v-if="updateResults.length > 0" class="result-section animate-in animate-in-delay-5">
        <h3 class="section-title">📝 动态 <span class="result-count">{{ updateResults.length }}</span></h3>
        <div class="result-list">
          <router-link
            v-for="item in updateResults"
            :key="'upd-' + item.id"
            :to="'/updates'"
            class="result-card"
          >
            <div class="result-title">{{ highlightMatch(item.title) }}</div>
            <div class="result-excerpt">{{ highlightMatch(item.content) }}</div>
            <div class="result-meta">
              <span>{{ item.date }}</span>
              <span v-for="tag in item.tags" :key="tag" class="result-tag">{{ tag }}</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- 成就结果 -->
      <div v-if="achievementResults.length > 0" class="result-section animate-in animate-in-delay-6">
        <h3 class="section-title">🏆 成就 <span class="result-count">{{ achievementResults.length }}</span></h3>
        <div class="result-list">
          <router-link
            v-for="item in achievementResults"
            :key="'ach-' + item.id"
            :to="'/achievement/' + item.slug"
            class="result-card"
          >
            <div class="result-title">{{ highlightMatch(item.title) }}</div>
            <div class="result-excerpt" v-if="item.summary">{{ highlightMatch(item.summary) }}</div>
            <div class="result-meta">
              <span>{{ item.date }}</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- 无结果 -->
      <div v-if="totalResults === 0" class="empty-state animate-in animate-in-delay-2">
        <div class="empty-icon">😕</div>
        <div class="empty-text">没有找到相关内容</div>
        <div class="empty-hint">试试其他关键词</div>
      </div>
    </div>

    <!-- 初始状态 -->
    <div v-if="!query" class="search-tips animate-in animate-in-delay-2">
      <div class="tip-card">
        <span class="tip-icon">💡</span>
        <span>可以搜索：博客标题、项目名称、文件描述...</span>
      </div>
      <div class="tip-card">
        <span class="tip-icon">🏷️</span>
        <span>支持按标签搜索：Vue、Python、Go...</span>
      </div>
      <div class="popular-tags">
        <span class="popular-label">热门标签：</span>
        <span
          v-for="tag in popularTags"
          :key="tag"
          class="popular-tag"
          @click="query = tag; doSearch()"
        >{{ tag }}</span>
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE = '/api'

export default {
  name: 'SearchPage',
  data() {
    return {
      query: '',
      searching: false,
      blogs: [],
      projects: [],
      files: [],
      updates: [],
      achievements: [],
      popularTags: ['Vue', 'Python', 'Go', 'Rust', 'Docker', 'Linux', 'AI']
    }
  },
  computed: {
    blogResults() {
      return this.filterItems(this.blogs, ['title', 'summary', 'content', 'tags'])
    },
    projectResults() {
      return this.filterItems(this.projects, ['title', 'description', 'tech'])
    },
    fileResults() {
      return this.filterItems(this.files, ['name', 'description'])
    },
    updateResults() {
      return this.filterItems(this.updates, ['title', 'content', 'tags'])
    },
    achievementResults() {
      return this.filterItems(this.achievements, ['title', 'summary', 'content'])
    },
    totalResults() {
      return this.blogResults.length + this.projectResults.length +
             this.fileResults.length + this.updateResults.length +
             this.achievementResults.length
    }
  },
  methods: {
    filterItems(items, fields) {
      if (!this.query.trim()) return []
      const q = this.query.toLowerCase()
      return items.filter(item => {
        return fields.some(field => {
          const val = item[field]
          if (Array.isArray(val)) {
            return val.some(v => String(v).toLowerCase().includes(q))
          }
          return String(val || '').toLowerCase().includes(q)
        })
      })
    },
    highlightMatch(text) {
      if (!text || !this.query.trim()) return text
      const q = this.query.trim()
      const regex = new RegExp(`(${q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi')
      const parts = String(text).split(regex)
      return parts.map((part, i) => {
        if (part.toLowerCase() === q.toLowerCase()) {
          return `<mark class="highlight">${part}</mark>`
        }
        return part
      }).join('')
    },
    doSearch() {
      if (!this.query.trim()) return
      this.searching = true
      // 搜索是本地过滤，数据已加载
      this.$nextTick(() => {
        this.searching = false
      })
    },
    clearSearch() {
      this.query = ''
      this.$refs.searchInput?.focus()
    },
    async loadData() {
      try {
        const [blogs, projects, files, updates, achievements] = await Promise.all([
          fetch(`${API_BASE}/blogs`).then(r => r.json()),
          fetch(`${API_BASE}/projects`).then(r => r.json()),
          fetch(`${API_BASE}/files`).then(r => r.json()),
          fetch(`${API_BASE}/updates`).then(r => r.json()),
          fetch(`${API_BASE}/achievements`).then(r => r.json())
        ])
        this.blogs = Array.isArray(blogs) ? blogs : (blogs.data || [])
        this.projects = Array.isArray(projects) ? projects : (projects.data || [])
        // files 可能返回 {data: [...]}
        this.files = Array.isArray(files) ? files : (files.data || [])
        this.updates = Array.isArray(updates) ? updates : (updates.data || [])
        this.achievements = Array.isArray(achievements) ? achievements : (achievements.data || [])
      } catch (e) {
        console.error('搜索数据加载失败:', e)
      }
    }
  },
  mounted() {
    this.loadData()
    this.$nextTick(() => {
      this.$refs.searchInput?.focus()
    })
  }
}
</script>

<style scoped>
.search-page {
  padding: 32px 16px;
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

/* 搜索框 */
.search-box {
  max-width: 600px;
  margin: 0 auto 32px;
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  background: var(--card-bg, #fff);
  border: 2px solid var(--border, #e2e8f0);
  border-radius: 16px;
  padding: 4px 16px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.search-input-wrapper:focus-within {
  border-color: #4f46e5;
  box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
}

.search-icon {
  font-size: 1.2rem;
  margin-right: 10px;
  opacity: 0.5;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 1.1rem;
  padding: 14px 0;
  background: transparent;
  color: var(--text-primary, #0f172a);
  font-family: inherit;
}

.search-input::placeholder {
  color: var(--text-muted, #94a3b8);
}

.search-clear {
  background: none;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  padding: 4px 8px;
  color: var(--text-muted, #94a3b8);
  border-radius: 50%;
}

.search-clear:hover {
  background: var(--bg, #f1f5f9);
  color: var(--text-primary, #0f172a);
}

/* 搜索中 */
.searching-indicator {
  text-align: center;
  color: var(--text-muted, #94a3b8);
  padding: 20px;
  animation: pulse 1.5s ease infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

/* 结果统计 */
.result-stats {
  text-align: center;
  margin-bottom: 24px;
  color: var(--text-secondary, #64748b);
  font-size: 0.95rem;
}

.result-stats strong {
  color: var(--text-primary, #0f172a);
}

/* 分类标题 */
.result-section {
  margin-bottom: 28px;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.result-count {
  font-size: 0.8rem;
  background: var(--bg, #f1f5f9);
  padding: 2px 8px;
  border-radius: 999px;
  color: var(--text-secondary, #64748b);
  font-weight: 500;
}

/* 结果卡片 */
.result-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.result-card {
  display: block;
  padding: 16px;
  background: var(--card-bg, #fff);
  border: 1px solid var(--border, #e2e8f0);
  border-radius: 12px;
  text-decoration: none !important;
  transition: all 0.2s ease;
}

.result-card:hover {
  border-color: #4f46e5;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.1);
  transform: translateY(-1px);
}

.result-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary, #0f172a);
  margin-bottom: 4px;
}

.result-excerpt {
  font-size: 0.85rem;
  color: var(--text-secondary, #64748b);
  margin-bottom: 8px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.result-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  font-size: 0.8rem;
  color: var(--text-muted, #94a3b8);
}

.result-tag {
  padding: 1px 6px;
  background: var(--bg, #f1f5f9);
  border-radius: 4px;
  font-size: 0.75rem;
}

.result-status {
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.result-status.进行中 {
  background: #fef3c7;
  color: #92400e;
}

.result-status.已完成 {
  background: #d1fae5;
  color: #065f46;
}

/* 高亮 */
:deep(.highlight) {
  background: #fef08a;
  color: #0f172a;
  padding: 1px 2px;
  border-radius: 2px;
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

/* 搜索提示 */
.search-tips {
  max-width: 500px;
  margin: 0 auto;
}

.tip-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: var(--card-bg, #fff);
  border: 1px solid var(--border, #e2e8f0);
  border-radius: 10px;
  margin-bottom: 8px;
  font-size: 0.9rem;
  color: var(--text-secondary, #64748b);
}

.tip-icon {
  font-size: 1.2rem;
}

.popular-tags {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 16px;
  padding: 12px 16px;
}

.popular-label {
  font-size: 0.85rem;
  color: var(--text-muted, #94a3b8);
}

.popular-tag {
  padding: 4px 12px;
  background: var(--card-bg, #fff);
  border: 1px solid var(--border, #e2e8f0);
  border-radius: 999px;
  font-size: 0.85rem;
  cursor: pointer;
  color: var(--text-secondary, #64748b);
  transition: all 0.2s;
}

.popular-tag:hover {
  border-color: #4f46e5;
  color: #4f46e5;
  background: rgba(79, 70, 229, 0.05);
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
.animate-in-delay-5 { animation-delay: 0.5s; }
.animate-in-delay-6 { animation-delay: 0.6s; }

@keyframes slideUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
