<template>
  <div class="blog-detail-page">
    <div class="blog-back">
      <router-link to="/blogs" class="back-link">← 返回博客列表</router-link>
    </div>

    <div class="bento-card blog-content animate-in" v-if="blog">
      <div class="blog-meta">
        <span class="blog-date">📅 {{ blog.date }}</span>
      </div>
      <h1 class="blog-title">{{ blog.title }}</h1>
      <div class="blog-tags">
        <span class="bento-tag" v-for="tag in blog.tags" :key="tag">{{ tag }}</span>
      </div>
      <div class="blog-body">
        <p>{{ blog.content }}</p>
      </div>
    </div>

    <div class="bento-card empty-placeholder" v-else>
      <p>📭 文章未找到</p>
    </div>
  </div>
</template>

<script>
import blogsData from '../data/blogs.json'

export default {
  name: 'BlogDetailPage',
  data() {
    return {
      blog: null
    }
  },
  mounted() {
    const slug = this.$route.params.slug
    this.blog = blogsData.find(b => b.slug === slug) || null
  }
}
</script>

<style scoped>
.blog-detail-page {
  max-width: 720px;
  margin: 0 auto;
}

.blog-back {
  margin-bottom: 20px;
}

.back-link {
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-secondary);
  transition: color 0.2s;
}

.back-link:hover {
  color: var(--primary);
}

.blog-content {
  padding: 32px;
}

.blog-meta {
  margin-bottom: 12px;
}

.blog-date {
  font-size: 0.9rem;
  color: var(--text-muted);
}

.blog-title {
  font-size: 1.8rem;
  font-weight: 800;
  margin-bottom: 12px;
  line-height: 1.3;
}

.blog-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 24px;
}

.blog-body {
  font-size: 1.05rem;
  line-height: 1.8;
  color: var(--text-secondary);
}

.blog-body p {
  margin-bottom: 16px;
}

.empty-placeholder {
  text-align: center;
  padding: 48px;
  color: var(--text-muted);
  font-size: 1.1rem;
}
</style>
