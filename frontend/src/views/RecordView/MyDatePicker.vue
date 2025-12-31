<script lang="ts" setup>
const props = defineProps<{
  disabled?: boolean
}>()
</script>

<template>
  <div class="w-full grid grid-cols-[4rem_auto_4rem]">
    <van-button plain :disabled icon="arrow-left" />
    <div class="text-center">date</div>
    <van-button plain :disabled icon="arrow" />
  </div>
</template>
