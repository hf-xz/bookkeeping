<script lang="ts" setup>
const router = useRouter()
const tabs = router
  .getRoutes()
  .filter((route) => route.meta.tabbar)
  .map((route) => ({
    route: route.path,
    icon: route.meta.icon as string,
    title: route.meta.title,
  }))
</script>

<template>
  <van-tabbar route :fixed="false" :safe-area-inset-bottom="true">
    <van-tabbar-item v-for="tab in tabs" :key="tab.route" replace :to="tab.route" :icon="tab.icon">
      {{ tab.title }}
    </van-tabbar-item>
  </van-tabbar>
</template>
