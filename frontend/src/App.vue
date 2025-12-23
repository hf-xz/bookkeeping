<script setup lang="ts">
const handleClick = () => {
  showToast('You clicked the Vant Button!')
}
</script>

<template>
  <h1>You did it!</h1>
  <p>
    Visit <a href="https://vuejs.org/" target="_blank" rel="noopener">vuejs.org</a> to read the
    documentation
  </p>
  <van-button type="primary" @click="handleClick">Vant Button</van-button>
</template>

<style scoped></style>
