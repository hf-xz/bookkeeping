<script setup lang="ts">
import AppTabbar from '@/components/layouts/AppTabbar.vue'
</script>

<template>
  <main class="h-screen flex flex-col bg-gray-50">
    <div class="flex-1 overflow-auto p-4">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </div>
    <app-tabbar />
  </main>
</template>

<style>
@import '@/style.css';
</style>
