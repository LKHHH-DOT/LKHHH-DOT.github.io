<template>
  <div class="splash-screen" :class="{ 'splash-exit': exiting }">
    <!-- 背景粒子动画 -->
    <div class="particles">
      <div v-for="i in 30" :key="i" class="particle" :style="particleStyle(i)"></div>
    </div>

    <!-- 主内容 -->
    <div class="splash-content">
      <!-- Logo 动画 -->
      <div class="logo-wrapper">
        <div class="logo-icon">🦞</div>
        <div class="logo-ring"></div>
      </div>

      <!-- 标题 -->
      <h1 class="splash-title">
        <span v-for="(char, idx) in titleChars" :key="idx"
              class="title-char"
              :style="{ animationDelay: `${0.3 + idx * 0.08}s` }">
          {{ char }}
        </span>
      </h1>

      <!-- 副标题 -->
      <p class="splash-subtitle">欢迎来到我的世界</p>

      <!-- 加载进度条 -->
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progress + '%' }"></div>
      </div>

      <p class="splash-tip">{{ tips[currentTip] }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SplashScreen',
  data() {
    return {
      exiting: false,
      progress: 0,
      currentTip: 0,
      titleChars: '小熙'.split(''),
      tips: [
        '加载中，请稍候...',
        '正在准备精彩内容...',
        '马上就好...',
        '即将为你呈现 ✨'
      ]
    }
  },
  methods: {
    particleStyle(i) {
      const size = Math.random() * 4 + 2
      return {
        width: `${size}px`,
        height: `${size}px`,
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        animationDelay: `${Math.random() * 3}s`,
        animationDuration: `${3 + Math.random() * 4}s`
      }
    },
    startLoading() {
      // 进度条动画
      const interval = setInterval(() => {
        // 前快后慢，模拟真实加载
        const increment = this.progress < 50 ? 3 + Math.random() * 5
                        : this.progress < 80 ? 1 + Math.random() * 3
                        : 0.3 + Math.random() * 0.8
        this.progress = Math.min(this.progress + increment, 100)

        // 切换提示文字
        if (this.progress > 30 && this.currentTip < 1) this.currentTip = 1
        if (this.progress > 60 && this.currentTip < 2) this.currentTip = 2
        if (this.progress > 85 && this.currentTip < 3) this.currentTip = 3

        if (this.progress >= 100) {
          clearInterval(interval)
          // 完成，等待一下再退出
          setTimeout(() => {
            this.exiting = true
            // 动画结束后通知父组件
            setTimeout(() => {
              this.$emit('finished')
            }, 800)
          }, 500)
        }
      }, 100)
    }
  },
  mounted() {
    this.startLoading()
  }
}
</script>

<style scoped>
.splash-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  overflow: hidden;
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.splash-exit {
  opacity: 0;
  transform: scale(1.1);
  pointer-events: none;
}

/* 粒子背景 */
.particles {
  position: absolute;
  inset: 0;
}

.particle {
  position: absolute;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  animation: float linear infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) scale(1);
    opacity: 0.3;
  }
  50% {
    transform: translateY(-30px) scale(1.5);
    opacity: 0.8;
  }
}

/* Logo */
.logo-wrapper {
  position: relative;
  width: 100px;
  height: 100px;
  margin: 0 auto 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-icon {
  font-size: 3.5rem;
  animation: logoBounce 1.5s ease-in-out infinite;
  z-index: 2;
  position: relative;
}

@keyframes logoBounce {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-10px) scale(1.1); }
}

.logo-ring {
  position: absolute;
  inset: -8px;
  border: 3px solid transparent;
  border-top-color: #a78bfa;
  border-right-color: #60a5fa;
  border-radius: 50%;
  animation: spin 1.5s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 标题逐字动画 */
.splash-content {
  text-align: center;
  z-index: 1;
}

.splash-title {
  font-size: 3rem;
  font-weight: 800;
  color: white;
  margin: 0 0 12px;
  letter-spacing: 4px;
}

.title-char {
  display: inline-block;
  opacity: 0;
  transform: translateY(20px);
  animation: charAppear 0.5s ease forwards;
}

@keyframes charAppear {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.splash-subtitle {
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.1rem;
  margin: 0 0 40px;
  letter-spacing: 6px;
  animation: fadeIn 1s ease 0.8s both;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 进度条 */
.progress-bar {
  width: 240px;
  height: 4px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 4px;
  margin: 0 auto 16px;
  overflow: hidden;
  animation: fadeIn 1s ease 0.5s both;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
  border-radius: 4px;
  transition: width 0.15s ease;
  box-shadow: 0 0 10px rgba(96, 165, 250, 0.5);
}

.splash-tip {
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.85rem;
  animation: fadeIn 1s ease 0.5s both;
  transition: opacity 0.3s;
}
</style>
