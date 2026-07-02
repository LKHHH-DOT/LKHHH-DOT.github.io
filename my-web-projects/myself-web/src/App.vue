<template>
  <div id="app" :class="{ 'dark-mode': isDark }">
    <!-- 开机动画 -->
    <SplashScreen v-if="showSplash" @finished="onSplashFinished" />

    <template v-if="!showSplash">
      <!-- ===== 顶部导航栏 ===== -->
      <nav class="navbar" :class="{ scrolled: isScrolled }">
        <div class="nav-inner">
          <div class="nav-left">
            <button class="sidebar-toggle" @click="sidebarOpen = !sidebarOpen" title="菜单">
              <span class="hamburger" :class="{ active: sidebarOpen }">
                <span></span><span></span><span></span>
              </span>
            </button>
            <router-link to="/" class="logo">
              <span class="logo-icon">🦞</span>
              <span class="logo-text gradient-text">小熙</span>
            </router-link>
          </div>

          <div class="nav-links">
            <template v-for="item in topNav" :key="item.label">
              <a v-if="item.link" :href="item.link" target="_blank" rel="noopener" class="nav-link">
                <span class="nav-icon">{{ item.icon }}</span>
                <span class="nav-label">{{ item.label }}</span>
              </a>
              <router-link v-else :to="item.path" class="nav-link" active-class="nav-link-active">
                <span class="nav-icon">{{ item.icon }}</span>
                <span class="nav-label">{{ item.label }}</span>
              </router-link>
            </template>
          </div>

          <div class="nav-actions">
            <button class="theme-toggle" @click="toggleTheme" :title="isDark ? '亮色' : '暗色'">
              {{ isDark ? '☀️' : '🌙' }}
            </button>
          </div>
        </div>
      </nav>

      <!-- ===== 主体 ===== -->
      <div class="layout">
        <div class="sidebar-overlay" v-if="sidebarOpen" @click="sidebarOpen = false"></div>

        <aside class="sidebar" :class="{ open: sidebarOpen }">
          <div class="sidebar-header">
            <span class="sidebar-title">📋 全部菜单</span>
            <button class="sidebar-close" @click="sidebarOpen = false">✕</button>
          </div>

          <!-- 常用（含外链） -->
          <div class="sidebar-section">
            <div class="sidebar-label">📌 常用</div>
            <router-link
              v-for="item in topNav.filter(n => !n.link)"
              :key="'top-' + item.label"
              :to="item.path"
              class="sidebar-link"
              active-class="sidebar-link-active"
              @click="sidebarOpen = false"
            >
              <span class="sidebar-icon">{{ item.icon }}</span>
              <span class="sidebar-text">{{ item.label }}</span>
            </router-link>
            <a
              v-for="item in topNav.filter(n => n.link)"
              :key="'ext-' + item.label"
              :href="item.link"
              target="_blank"
              rel="noopener"
              class="sidebar-link"
              @click="sidebarOpen = false"
            >
              <span class="sidebar-icon">{{ item.icon }}</span>
              <span class="sidebar-text">{{ item.label }}</span>
            </a>
          </div>

          <div class="sidebar-divider"></div>

          <!-- 更多 -->
          <div class="sidebar-section">
            <div class="sidebar-label">📂 更多</div>
            <router-link
              v-for="item in sideNav"
              :key="item.label"
              :to="item.path"
              class="sidebar-link"
              active-class="sidebar-link-active"
              @click="sidebarOpen = false"
            >
              <span class="sidebar-icon">{{ item.icon }}</span>
              <span class="sidebar-text">{{ item.label }}</span>
            </router-link>
          </div>

          <div class="sidebar-footer">
            <span>🦞 lazaxa.cn</span>
          </div>
        </aside>

        <main class="main-content">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </main>
      </div>

      <footer class="footer">
        <div class="footer-inner">
          <p>© {{ year }} 小熙 · Built with Vue 3</p>
          <div class="footer-links">
            <a href="https://github.com/" target="_blank" rel="noopener">GitHub</a>
            <span class="footer-dot">·</span>
            <span>lazaxa.cn</span>
          </div>
        </div>
      </footer>
    </template>
  </div>
</template>

<script>
import SplashScreen from './components/SplashScreen.vue'

export default {
  name: 'App',
  components: { SplashScreen },
  data() {
    return {
      showSplash: true,
      isScrolled: false,
      isDark: false,
      sidebarOpen: false,
      topNav: [
        { path: '/', label: '首页', icon: '👤' },
        { path: '/search', label: '搜索', icon: '🔍' },
        { path: '/projects', label: '项目', icon: '📦' },
        { path: '/blogs', label: '博客', icon: '📖' },
        { path: '/ai/chat', label: 'AI 对话', icon: '🤖' },
        { label: 'GitHub', icon: '🐙', link: 'https://github.com/' }
      ],
      sideNav: [
        { path: '/achievements', label: '成就', icon: '🏆' },
        { path: '/updates', label: '动态', icon: '📝' },
        { path: '/status', label: '状态', icon: '⏰' },
        { path: '/stats', label: '统计', icon: '📊' },
        { path: '/files', label: '文件', icon: '📁' },
        { path: '/guestbook', label: '留言', icon: '💬' },
        { path: '/links', label: '友链', icon: '🌐' },
        { path: '/gallery', label: '相册', icon: '🖼️' },
        { path: '/ai/image', label: 'AI 绘画', icon: '🎨' }
      ]
    }
  },
  computed: {
    year() { return new Date().getFullYear() }
  },
  methods: {
    onSplashFinished() {
      console.log('[Splash] finished event received')
      this.showSplash = false
    },
    toggleTheme() {
      this.isDark = !this.isDark
      localStorage.setItem('theme', this.isDark ? 'dark' : 'light')
      this.applyTheme()
    },
    applyTheme() {
      document.documentElement.classList.toggle('dark', this.isDark)
    },
    detectTheme() {
      const saved = localStorage.getItem('theme')
      if (saved) {
        this.isDark = saved === 'dark'
      } else {
        this.isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      }
      this.applyTheme()
    },
    handleScroll() {
      this.isScrolled = window.scrollY > 20
    }
  },
  mounted() {
    this.detectTheme()
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
  }
}
</script>

<style>
/* ===== 导航栏 ===== */
.navbar {
  position: sticky;
  top: 16px;
  z-index: 100;
  padding: 0 16px;
  margin-top: 16px;
  transition: all 0.3s ease;
}
.navbar.scrolled {
  top: 0;
  margin-top: 0;
  padding: 0;
}
.nav-inner {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 16px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(226, 232, 240, 0.6);
  border-radius: 20px;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07);
  transition: all 0.3s ease;
}
.navbar.scrolled .nav-inner {
  border-radius: 0;
  border-left: none;
  border-right: none;
  border-top: none;
  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08);
}
.nav-left {
  display: flex;
  align-items: center;
  gap: 8px;
}
.sidebar-toggle {
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.sidebar-toggle:hover {
  background: #f1f5f9;
}
.hamburger {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 20px;
  height: 16px;
  justify-content: center;
}
.hamburger span {
  display: block;
  height: 2px;
  background: #0f172a;
  border-radius: 2px;
  transition: all 0.3s ease;
}
.hamburger.active span:nth-child(1) {
  transform: rotate(45deg) translate(4px, 4px);
}
.hamburger.active span:nth-child(2) {
  opacity: 0;
}
.hamburger.active span:nth-child(3) {
  transform: rotate(-45deg) translate(4px, -4px);
}
.logo {
  display: flex;
  align-items: center;
  gap: 6px;
  text-decoration: none !important;
  cursor: pointer;
  user-select: none;
}
.logo-icon { font-size: 1.4rem; }
.logo-text {
  font-size: 1.15rem;
  font-weight: 800;
  background: linear-gradient(135deg, #4f46e5, #818cf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.nav-links { display: flex; gap: 2px; }
.nav-link {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 7px 12px;
  border-radius: 12px;
  color: #64748b !important;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s ease;
  text-decoration: none !important;
}
.nav-link:hover {
  background: #f1f5f9;
  color: #0f172a !important;
}
.nav-link-active {
  background: linear-gradient(135deg, #4f46e5, #818cf8) !important;
  color: white !important;
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3);
}
.nav-icon { font-size: 1rem; }
.nav-actions { display: flex; align-items: center; gap: 8px; }
.theme-toggle {
  background: none;
  border: none;
  font-size: 1.15rem;
  cursor: pointer;
  padding: 6px;
  border-radius: 50%;
  line-height: 1;
}
.theme-toggle:hover {
  background: #f1f5f9;
  transform: scale(1.1);
}

/* ===== 布局 ===== */
.layout {
  position: relative;
  max-width: 960px;
  margin: 0 auto;
}
.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 90;
  animation: fadeIn 0.2s ease;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* ===== 侧边栏 ===== */
.sidebar {
  position: fixed;
  top: 0;
  left: -280px;
  width: 260px;
  height: 100vh;
  background: #ffffff;
  border-right: 1px solid #e2e8f0;
  z-index: 95;
  display: flex;
  flex-direction: column;
  transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
  overflow-y: auto;
}
.sidebar.open { left: 0; }
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 20px 12px;
  border-bottom: 1px solid #e2e8f0;
}
.sidebar-title { font-size: 1rem; font-weight: 700; }
.sidebar-close {
  background: none;
  border: none;
  font-size: 1.1rem;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 8px;
  color: #64748b;
}
.sidebar-close:hover {
  background: #f1f5f9;
  color: #0f172a;
}
.sidebar-section { padding: 8px 12px; }
.sidebar-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 8px 8px 4px;
}
.sidebar-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 12px;
  color: #64748b !important;
  font-size: 0.9rem;
  font-weight: 500;
  text-decoration: none !important;
  transition: all 0.15s ease;
}
.sidebar-link:hover {
  background: #f1f5f9;
  color: #0f172a !important;
}
.sidebar-link-active {
  background: #eef2ff !important;
  color: #4f46e5 !important;
  font-weight: 600;
}
.sidebar-icon {
  font-size: 1.1rem;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
}
.sidebar-text { flex: 1; }
.sidebar-divider {
  height: 1px;
  background: #e2e8f0;
  margin: 4px 16px;
}
.sidebar-footer {
  margin-top: auto;
  padding: 16px 20px;
  border-top: 1px solid #e2e8f0;
  text-align: center;
  font-size: 0.8rem;
  color: #94a3b8;
}

/* ===== 主内容 ===== */
.main-content {
  padding: 24px 20px 40px;
  min-height: calc(100vh - 120px);
}

/* ===== 页脚 ===== */
.footer {
  border-top: 1px solid #e2e8f0;
  padding: 24px 20px;
  margin-top: 40px;
}
.footer-inner {
  max-width: 960px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  color: #94a3b8;
}
.footer-links { display: flex; align-items: center; gap: 8px; }
.footer-links a { color: #64748b; transition: color 0.2s; }
.footer-links a:hover { color: #4f46e5; }
.footer-dot { color: #e2e8f0; }

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .nav-label { display: none; }
  .nav-link { padding: 7px 10px; }
  .main-content { padding: 20px 16px 40px; }
  .footer-inner {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
}
@media (min-width: 769px) {
  .nav-label { display: inline; }
}

/* ===== 深色模式 ===== */
.dark .nav-inner {
  background: rgba(30, 41, 59, 0.85);
  border-color: rgba(51, 65, 85, 0.6);
}
.dark .sidebar-toggle:hover { background: #1e293b; }
.dark .hamburger span { background: #f1f5f9; }
.dark .nav-link { color: #94a3b8 !important; }
.dark .nav-link:hover { background: #1e293b; color: #f1f5f9 !important; }
.dark .theme-toggle:hover { background: #1e293b; }
.dark .sidebar {
  background: #1e293b;
  border-right-color: #334155;
}
.dark .sidebar-header { border-bottom-color: #334155; }
.dark .sidebar-close { color: #94a3b8; }
.dark .sidebar-close:hover { background: #0f172a; color: #f1f5f9; }
.dark .sidebar-label { color: #64748b; }
.dark .sidebar-link { color: #94a3b8 !important; }
.dark .sidebar-link:hover { background: #0f172a; color: #f1f5f9 !important; }
.dark .sidebar-link-active {
  background: rgba(79, 70, 229, 0.15) !important;
  color: #818cf8 !important;
}
.dark .sidebar-divider { background: #334155; }
.dark .sidebar-footer { border-top-color: #334155; color: #64748b; }
.dark .footer { border-top-color: #334155; }
.dark .footer-inner { color: #64748b; }
.dark .footer-links a { color: #94a3b8; }
.dark .footer-links a:hover { color: #818cf8; }
.dark .footer-dot { color: #334155; }
</style>
