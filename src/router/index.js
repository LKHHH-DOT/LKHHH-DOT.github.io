import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Achievements from '../views/Achievements.vue'
import AchievementDetail from '../views/AchievementDetail.vue'
import Updates from '../views/Updates.vue'
import AIChat from '../views/AIChat.vue'
import AIImage from '../views/AIImage.vue'
import Projects from '../views/Projects.vue'
import SeriesDetail from '../views/SeriesDetail.vue'
import Blogs from '../views/Blogs.vue'
import BlogDetail from '../views/BlogDetail.vue'
import Status from '../views/Status.vue'
import Stats from '../views/Stats.vue'
import Files from '../views/Files.vue'
import Search from '../views/Search.vue'
import Guestbook from '../views/Guestbook.vue'
import Links from '../views/Links.vue'
import Gallery from '../views/Gallery.vue'
import VncGuide from '../views/VncGuide.vue'

const routes = [
  { path: '/', name: 'Home', component: Home, meta: { title: '个人信息' } },
  { path: '/achievements', name: 'Achievements', component: Achievements, meta: { title: '重要成就' } },
  { path: '/achievement/:slug', name: 'AchievementDetail', component: AchievementDetail, meta: { title: '成就详情' } },
  { path: '/updates', name: 'Updates', component: Updates, meta: { title: '动态更新' } },
  { path: '/projects', name: 'Projects', component: Projects, meta: { title: '项目作品' } },
  { path: '/series/:slug', name: 'SeriesDetail', component: SeriesDetail, meta: { title: '系列详情' } },
  { path: '/blogs', name: 'Blogs', component: Blogs, meta: { title: '技术博客' } },
  { path: '/blog/:slug', name: 'BlogDetail', component: BlogDetail, meta: { title: '文章详情' } },
  { path: '/status', name: 'Status', component: Status, meta: { title: '在线状态' } },
  { path: '/stats', name: 'Stats', component: Stats, meta: { title: '数据统计' } },
  { path: '/files', name: 'Files', component: Files, meta: { title: '文件分享' } },
  { path: '/search', name: 'Search', component: Search, meta: { title: '全站搜索' } },
  { path: '/guestbook', name: 'Guestbook', component: Guestbook, meta: { title: '留言板' } },
  { path: '/links', name: 'Links', component: Links, meta: { title: '友情链接' } },
  { path: '/gallery', name: 'Gallery', component: Gallery, meta: { title: '相册' } },
  { path: '/vnc-guide', name: 'VncGuide', component: VncGuide, meta: { title: 'VNC 配置指南' } },
  { path: '/ai/chat', name: 'AIChat', component: AIChat, meta: { title: 'AI 对话' } },
  { path: '/ai/image', name: 'AIImage', component: AIImage, meta: { title: 'AI 绘画' } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
