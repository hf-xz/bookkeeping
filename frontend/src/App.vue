<script setup lang="ts">
import AppNavbar from '@/components/layouts/AppNavbar.vue'
import AppTabbar from '@/components/layouts/AppTabbar.vue'
</script>

<template>
  <main class="h-dvh bg-gray-100 flex flex-col">
    <app-navbar />

    <div class="flex-1 overflow-auto">
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
