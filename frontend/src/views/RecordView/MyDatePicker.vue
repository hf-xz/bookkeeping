<script lang="ts" setup>
import dayjs from 'dayjs'
import { localeDateString } from '@/utils/date'

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

// 日历显示状态
const showCalendar = ref(false)

// 确认选择日期
const onConfirmCalendar = (val: Date) => {
  showCalendar.value = false
  date.value = dayjs(val).format('YYYY-MM-DD')
}
</script>

<template>
  <div class="w-full grid grid-cols-[4rem_auto_4rem] items-center">
    <van-button plain :disabled icon="arrow-left" @click="selectYesterday" />
    <span class="text-md text-center" @click="showCalendar = true">{{ localeDateString(date) }}</span>
    <van-button plain :disabled="disabled || date == today" icon="arrow" @click="selectTommorow" />

    <van-calendar
      v-model:show="showCalendar"
      :min-date="new Date(2020, 0, 1)"
      :max-date="new Date()"
      @confirm="onConfirmCalendar"
    />
  </div>
</template>
