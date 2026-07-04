<template>
  <div class="home-page">
    <!-- Hero 区域：头像 + 简介 -->
    <div class="bento-card hero-card glass animate-in">
      <div class="hero-content">
        <div class="hero-avatar">
          <div class="avatar-ring">
            <div class="avatar-placeholder">{{ nameChar }}</div>
          </div>
          <div class="avatar-status"></div>
        </div>
        <div class="hero-text">
          <h1 class="hero-name">
            <span class="gradient-text">{{ profile.name || '小熙' }}</span>
            <span class="hero-wave">👋</span>
          </h1>
          <p class="hero-nickname" v-if="profile.nickname">@{{ profile.nickname }}</p>
          <p class="hero-title">{{ profile.title || '开发者 / 学生' }}</p>
          <p class="hero-bio">{{ profile.bio || '努力成为一个更好的自己 🚀' }}</p>
          <p class="hero-location" v-if="profile.location">📍 {{ profile.location }}</p>
        </div>
      </div>
    </div>

    <!-- Bento 网格布局 -->
    <div class="bento-grid bento-grid-2">
      <!-- 联系方式 -->
      <div class="bento-card animate-in animate-in-delay-1">
        <h3 class="bento-title">📬 联系方式</h3>
        <div class="contact-list">
          <div class="contact-item" v-for="(value, key) in profile.contact" :key="key">
            <span class="contact-icon">{{ contactIcons[key] || '📧' }}</span>
            <div class="contact-info">
              <span class="contact-label">{{ contactLabels[key] || key }}</span>
              <span class="contact-value" :class="{ empty: !value }">
                {{ value || '待填写' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 技能 -->
      <div class="bento-card animate-in animate-in-delay-2">
        <h3 class="bento-title">🛠️ 技能</h3>
        <div class="tags-cloud" v-if="profile.skills && profile.skills.length">
          <span class="bento-tag skill" v-for="skill in profile.skills" :key="skill">
            {{ skill }}
          </span>
        </div>
        <div class="empty-placeholder" v-else>
          <span>✨ 技能待补充</span>
        </div>
      </div>

      <!-- 兴趣爱好 -->
      <div class="bento-card animate-in animate-in-delay-3">
        <h3 class="bento-title">🎯 兴趣爱好</h3>
        <div class="tags-cloud" v-if="profile.interests && profile.interests.length">
          <span class="bento-tag interest" v-for="interest in profile.interests" :key="interest">
            {{ interest }}
          </span>
        </div>
        <div class="empty-placeholder" v-else>
          <span>🎨 兴趣待补充</span>
        </div>
      </div>

      <!-- 教育经历 -->
      <div class="bento-card animate-in animate-in-delay-4">
        <h3 class="bento-title">🎓 教育经历</h3>
        <div class="edu-timeline" v-if="profile.education && profile.education.length">
          <div class="edu-item" v-for="(edu, idx) in profile.education" :key="idx">
            <div class="edu-dot"></div>
            <div class="edu-content">
              <h4 class="edu-school">{{ edu.school }}</h4>
              <p class="edu-major">{{ edu.degree }} · {{ edu.major }}</p>
              <span class="edu-period">{{ edu.period }}</span>
            </div>
          </div>
        </div>
        <div class="empty-placeholder" v-else>
          <span>📚 教育经历待补充</span>
        </div>
      </div>
    </div>

    <!-- 底部装饰 -->
    <div class="home-decoration">
      <span>🦞</span>
      <span>·</span>
      <span>lazaxa.cn</span>
      <span>·</span>
      <span>🚀</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      profile: {
        name: '', nickname: '', avatar: '',
        title: '', bio: '', location: '',
        contact: { email: '', github: '', wechat: '', twitter: '', website: '' },
        education: [],
        skills: [],
        interests: []
      },
      contactIcons: {
        email: '📧', github: '💻', wechat: '💬',
        twitter: '🐦', website: '🌐'
      },
      contactLabels: {
        email: '邮箱', github: 'GitHub', wechat: '微信',
        twitter: 'Twitter', website: '网站'
      }
    }
  },
  computed: {
    nameChar() {
      const name = this.profile.name || '小熙'
      return name.charAt(0)
    }
  },
  mounted() {
    this.fetchProfile()
  },
  methods: {
    async fetchProfile() {
      try {
        const res = await fetch('/api/profile')
        if (res.ok) {
          this.profile = await res.json()
        }
      } catch (e) {
        console.warn('获取个人信息失败，使用默认值', e)
      }
    }
  }
}
</script>

<style scoped>
/* ===== Hero 区域 ===== */
.hero-card {
  margin-bottom: 20px;
  overflow: hidden;
  position: relative;
}

.hero-card::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(79, 70, 229, 0.08), transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.hero-content {
  display: flex;
  gap: 28px;
  align-items: center;
  position: relative;
  z-index: 1;
}

/* 头像 */
.hero-avatar {
  position: relative;
  flex-shrink: 0;
}

.avatar-ring {
  width: 130px;
  height: 130px;
  border-radius: 50%;
  padding: 5px;
  background: var(--gradient-primary);
  animation: ringSpin 4s linear infinite;
}

@keyframes ringSpin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.avatar-placeholder {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: var(--card-bg);
  color: var(--text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3.2rem;
  font-weight: 800;
}

.avatar-status {
  position: absolute;
  bottom: 6px;
  right: 6px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #22c55e;
  border: 3px solid var(--card-bg);
  box-shadow: 0 0 0 1px rgba(34, 197, 94, 0.3);
}

/* 文本 */
.hero-text {
  flex: 1;
}

.hero-name {
  font-size: 2.4rem;
  font-weight: 800;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.hero-wave {
  display: inline-block;
  animation: wave 2s ease-in-out infinite;
  transform-origin: 70% 70%;
}

@keyframes wave {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(15deg); }
  50% { transform: rotate(-10deg); }
  75% { transform: rotate(15deg); }
}

.hero-nickname {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-bottom: 4px;
}

.hero-title {
  color: var(--primary);
  font-weight: 600;
  font-size: 1.15rem;
  margin-bottom: 12px;
}

.hero-bio {
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.7;
  margin-bottom: 8px;
}

.hero-location {
  font-size: 0.95rem;
  color: var(--text-muted);
}

/* ===== 联系方式 ===== */
.contact-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 14px;
  background: var(--bg);
  border-radius: var(--radius-md);
  transition: all 0.2s;
}

.contact-item:hover {
  background: #eef2ff;
  transform: translateX(4px);
}

.contact-icon {
  font-size: 1.3rem;
  width: 32px;
  text-align: center;
}

.contact-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.contact-label {
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 500;
}

.contact-value {
  color: var(--text);
  font-weight: 600;
  font-size: 0.95rem;
  text-align: right;
  word-break: break-all;
}

.contact-value.empty {
  color: var(--text-muted);
  font-weight: 400;
  font-style: italic;
}

/* ===== 标签云 ===== */
.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* ===== 教育时间线 ===== */
.edu-timeline {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.edu-item {
  display: flex;
  gap: 14px;
  padding: 14px 0;
  border-bottom: 1px solid var(--border);
  position: relative;
}

.edu-item:last-child {
  border-bottom: none;
}

.edu-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--gradient-primary);
  margin-top: 6px;
  flex-shrink: 0;
}

.edu-content {
  flex: 1;
}

.edu-school {
  font-size: 1.05rem;
  font-weight: 600;
  margin-bottom: 4px;
}

.edu-major {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 4px;
}

.edu-period {
  display: inline-block;
  font-size: 0.85rem;
  color: var(--text-muted);
  background: var(--bg);
  padding: 3px 10px;
  border-radius: 6px;
}

/* ===== 空占位 ===== */
.empty-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  color: var(--text-muted);
  font-size: 0.9rem;
  background: var(--bg);
  border-radius: var(--radius-md);
  border: 2px dashed var(--border);
}

/* ===== 底部装饰 ===== */
.home-decoration {
  text-align: center;
  margin-top: 32px;
  color: var(--text-muted);
  font-size: 0.85rem;
  display: flex;
  justify-content: center;
  gap: 12px;
  opacity: 0.6;
}

@media (max-width: 600px) {
  .hero-content {
    flex-direction: column;
    text-align: center;
  }
  .hero-name {
    justify-content: center;
  }
  .contact-item {
    flex-direction: column;
    text-align: center;
  }
  .contact-info {
    flex-direction: column;
    text-align: center;
  }
  .contact-value {
    text-align: center;
  }
}
</style>
