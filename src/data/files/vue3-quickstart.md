# Vue 3 快速入门笔记

## 创建项目
npm create vue@latest

## Composition API 核心
import { ref, computed, watch } from 'vue'

const count = ref(0)
const double = computed(() => count.value * 2)

watch(count, (newVal, oldVal) => {
  console.log(\`count 从 \${oldVal} 变为 \${newVal}\`)
})

## 模板语法
- {{ title }} - 文本插值
- v-if / v-for - 条件/列表渲染
- @click / :href - 事件/属性绑定

## 生命周期
- onMounted - 挂载后
- onUpdated - 更新后
- onUnmounted - 卸载前

## 组件通信
- defineProps / defineEmits - 父子组件
- provide / inject - 跨层级
- Pinia - 全局状态管理
