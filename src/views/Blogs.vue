<template>
  <div class="blogs-page">
    <div class="page-header animate-in">
      <h1 class="page-title">📖 技术博客</h1>
      <p class="page-desc">记录学习中的思考与收获</p>
    </div>

    <div class="blog-list">
      <div
        class="bento-card blog-card animate-in"
        v-for="(blog, idx) in blogs"
        :key="blog.id"
        :style="{ animationDelay: `${idx * 0.1}s` }"
        @click="$router.push(`/blog/${blog.slug}`)"
      >
        <div class="blog-meta">
          <span class="blog-date">📅 {{ blog.date }}</span>
        </div>
        <h3 class="blog-title">{{ blog.title }}</h3>
        <p class="blog-summary">{{ blog.summary }}</p>
        <div class="blog-tags">
          <span class="bento-tag" v-for="tag in blog.tags" :key="tag">{{ tag }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import blogsData from '../data/blogs.json'

export default {
  name: 'BlogsPage',
  data() {
    return {
      blogs: blogsData
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

.blog-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.blog-card {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.blog-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
}

.blog-meta {
  margin-bottom: 8px;
}

.blog-date {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.blog-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--text);
}

.blog-summary {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 12px;
}

.blog-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
</style>
