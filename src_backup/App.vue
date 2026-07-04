<template>
  <div id="app">
    <!-- 开机动画 -->
    <SplashScreen v-if="showSplash" @finished="showSplash = false" />

    <!-- 主内容区域（动画结束后才显示） -->
    <template v-if="!showSplash">
      <!-- 导航栏 -->
      <nav class="navbar">
        <div class="nav-inner">
          <router-link to="/" class="logo">🦞 小熙</router-link>
          <div class="nav-links">
            <router-link
              v-for="item in navItems"
              :key="item.path"
              :to="item.path"
              class="nav-link"
              active-class="active"
            >
              {{ item.icon }} {{ item.label }}
            </router-link>
          </div>
          <!-- 部署模式开关 -->
          <div class="deploy-switch" :title="deployMode === 'local' ? '当前：本地开发模式' : '当前：公网部署模式'">
            <span class="switch-label">{{ deployMode === 'local' ? '🏠 本地' : '🌐 公网' }}</span>
            <label class="switch">
              <input type="checkbox" v-model="isPublic" @change="toggleDeployMode" />
              <span class="slider"></span>
            </label>
          </div>
        </div>
      </nav>

      <!-- 页面内容 -->
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>

      <!-- 页脚 -->
      <footer class="footer">
        <p>© {{ year }} 小熙 · Built with Vue 3</p>
        <p class="deploy-hint">
          {{ deployMode === 'local' ? '🏠 本地开发模式 · npm run dev' : '🌐 公网部署模式 · 已构建发布' }}
        </p>
      </footer>
    </template>
  </div>
</template>

<script>
import SplashScreen from './components/SplashScreen.vue'

export default {
  name: 'App',
  components: {
    SplashScreen
  },
  data() {
    return {
      showSplash: true,
      navItems: [
        { path: '/', label: '个人信息', icon: '👤' },
        { path: '/achievements', label: '重要成就', icon: '🏆' },
        { path: '/updates', label: '动态更新', icon: '📝' }
      ],
      deployMode: 'local',
      isPublic: false
    }
  },
  computed: {
    year() {
      return new Date().getFullYear()
    }
  },
  methods: {
    toggleDeployMode() {
      this.deployMode = this.isPublic ? 'public' : 'local'
      localStorage.setItem('deployMode', this.deployMode)
    },
    detectDeployMode() {
      const saved = localStorage.getItem('deployMode')
      if (saved) {
        this.deployMode = saved
        this.isPublic = saved === 'public'
        return
      }
      const host = window.location.hostname
      if (host === 'localhost' || host === '127.0.0.1' || host === '') {
        this.deployMode = 'local'
        this.isPublic = false
      } else {
        this.deployMode = 'public'
        this.isPublic = true
      }
    }
  },
  mounted() {
    this.detectDeployMode()
  }
}
</script>

<style scoped>
.navbar {
  background: var(--card-bg);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(8px);
  background: rgba(255,255,255,0.95);
}

.nav-inner {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 20px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text) !important;
}

.nav-links {
  display: flex;
  gap: 4px;
}

.nav-link {
  padding: 8px 14px;
  border-radius: 8px;
  color: var(--text-secondary) !important;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.nav-link:hover {
  background: #f1f5f9;
  color: var(--text) !important;
}

.nav-link.active {
  background: var(--primary);
  color: white !important;
}

.deploy-switch {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.switch-label {
  white-space: nowrap;
}

.switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 22px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: #cbd5e1;
  transition: 0.3s;
  border-radius: 22px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: var(--primary);
}

input:checked + .slider:before {
  transform: translateX(18px);
}

.main-content {
  max-width: 960px;
  margin: 0 auto;
  padding: 30px 20px;
  min-height: calc(100vh - 120px);
  animation: contentFadeIn 0.6s ease;
}

@keyframes contentFadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.footer {
  text-align: center;
  padding: 20px;
  color: var(--text-secondary);
  font-size: 0.85rem;
  border-top: 1px solid var(--border);
}

.deploy-hint {
  margin-top: 4px;
  font-size: 0.75rem;
  opacity: 0.7;
}
</style>
