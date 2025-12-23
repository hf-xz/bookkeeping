<script setup lang="ts">
import AppTabbar from '@/components/layouts/AppTabbar.vue'
</script>

<template>
  <main class="h-screen flex flex-col">
    <div class="flex-1 overflow-auto">
      <router-view />
    </div>
    <app-tabbar />
  </main>
</template>

<style>
@import '@/style.css';
</style>
