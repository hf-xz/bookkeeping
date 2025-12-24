import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      component: () => import('@/views/HomeView.vue'),
      path: '/',
      name: 'home',
    },
    {
      component: () => import('@/views/RecordView/index.vue'),
      path: '/record',
      name: 'record',
    },
  ],
})

export default router
