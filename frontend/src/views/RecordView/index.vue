<!-- RecordView  -->
<script lang="ts" setup>
import type { TransactionWithMetricName } from '@/models/transaction'
import DayRecordForm from './DayRecordForm.vue'
import MyDatePicker from './MyDatePicker.vue'

// 所有日期的记录缓存列表
const records = ref<Record<string, Array<TransactionWithMetricName>>>({})

// 更新记录缓存
const updateRecords = (txns: TransactionWithMetricName[], startDate: string, endDate: string) => {
  let day = startDate
  while (day <= endDate) {
    records.value[day] = txns.filter((t) => t.record_date === day)
    day = addDate(day, 1)
  }
}

// 当前选中的日期
const currentDate = ref<string>(getToday())
// 今日日期
const today = getToday()
// 表格编辑状态
const formEditing = ref(false)

// 更新指定日期的记录
const updateDateRecords = async (date: string) => {
  const res = await readOnedayTransactions(date)
  updateRecords(res, date, date)
}

onMounted(async () => {
  // 初始加载最近一周的记录
  const startDate = addDate(today, -6)
  const res = await readTransactions(startDate, today)
  updateRecords(res, startDate, today)

  // 监听日期变化，加载对应日期的记录
  // HACK 每次多加载一些日期，避免频繁请求
  watch(
    () => currentDate.value,
    (newDate) => {
      // 缓存没有才加载
      if (!records.value[newDate]) {
        updateDateRecords(newDate)
      }
    },
  )
})
</script>

<template>
  <main class="h-full flex flex-col p-4 gap-4">
    <MyDatePicker v-model:select-date="currentDate" :disabled="formEditing" />
    <DayRecordForm
      class="flex-1"
      v-model:formEditing="formEditing"
      :transactions="records[currentDate] || []"
      :date="currentDate"
      @upsert-success="updateDateRecords(currentDate)"
    />
  </main>
</template>
