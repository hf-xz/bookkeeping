<script lang="ts" setup>
const handleClick = () => {
  showToast('You clicked the Vant Button!')
}
</script>

<template>
  <van-button type="primary" @click="handleClick">Vant Button</van-button>
  <h1 class="text-3xl font-bold text-blue-600">Hello Tailwind</h1>
</template>
