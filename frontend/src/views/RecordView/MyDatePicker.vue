<script lang="ts" setup>
const props = defineProps<{
  selectDate: string
  disabled: boolean
}>()

const date = computed({
  get: () => props.selectDate,
  set: (val: string) => {
    emit('update:selectDate', val)
  },
})

const emit = defineEmits<{
  (e: 'update:selectDate', val: string): void
}>()

const selectYesterday = () => {
  date.value = addDate(date.value, -1)
}
const selectTommorow = () => {
  date.value = addDate(date.value, 1)
}

const today = getToday()
</script>

<template>
  <div class="w-full grid grid-cols-[4rem_auto_4rem] items-center">
    <van-button plain :disabled icon="arrow-left" @click="selectYesterday" />
    <span class="text-md text-center font-mono">{{ date }}</span>
    <van-button plain :disabled="disabled || date == today" icon="arrow" @click="selectTommorow" />
  </div>
</template>
