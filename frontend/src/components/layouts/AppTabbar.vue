<script lang="ts" setup>
const tabs = [
  {
    route: '/',
    icon: 'home-o',
    title: '首页',
  },
  {
    route: '/record',
    icon: 'orders-o',
    title: '记录',
  },
]
</script>

<template>
  <van-tabbar route>
    <van-tabbar-item v-for="tab in tabs" :key="tab.route" replace :to="tab.route" :icon="tab.icon">
      {{ tab.title }}
    </van-tabbar-item>
  </van-tabbar>
</template>
