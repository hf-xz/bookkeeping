import { createRouter, createWebHistory } from 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    title?: string
    tabbar?: boolean
    icon?: string
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      component: () => import('@/views/HomeView.vue'),
      path: '/',
      name: 'home',
      meta: { title: '首页', tabbar: true, icon: 'home-o' },
    },
    {
      component: () => import('@/views/RecordView/index.vue'),
      path: '/record',
      name: 'record',
      meta: { title: '记录', tabbar: true, icon: 'orders-o' },
    },
  ],
})

export default router
