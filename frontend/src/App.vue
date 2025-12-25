<script setup lang="ts">
import AppTabbar from '@/components/layouts/AppTabbar.vue'
const tabbarRef = ref<InstanceType<typeof AppTabbar> | null>(null)
const tabbarHeight = computed(() => tabbarRef.value?.$el.offsetHeight || 0)
</script>

<template>
  <main class="h-screen flex flex-col bg-gray-100">
    <!-- TODO title bar -->
    <!-- TODO content height -->
    <div class="flex-1 overflow-auto p-4" :style="{ marginBottom: tabbarHeight + 'px' }">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </div>
    <app-tabbar ref="tabbarRef" />
  </main>
</template>

<style>
@import '@/style.css';
</style>
