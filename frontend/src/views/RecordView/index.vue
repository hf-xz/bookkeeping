<!-- RecordView  -->
<script lang="ts" setup>
import type { TransactionWithMetricName } from '@/models/transaction'
import DayRecordForm from './DayRecordForm.vue'
import MyDatePicker from './MyDatePicker.vue'

// 所有日期的记录缓存列表
const records = ref<Record<string, Array<TransactionWithMetricName>>>({})

// 更新记录缓存
const updateRecords = (txns: TransactionWithMetricName[]) => {
  for (const txn of txns) {
    if (!records.value[txn.record_date]) {
      records.value[txn.record_date] = []
    }
    records.value[txn.record_date]!.push(txn)
  }
}

// 当前选中的日期
const currentDate = ref<string>(getToday())
// 今日日期
const today = getToday()

onMounted(async () => {
  // 初始加载最近一周的记录
  const startDate = addDate(today, -6)
  const res = await readTransactions(startDate, today)
  updateRecords(res)
})
</script>

<template>
  <main class="h-full flex flex-col p-4 gap-2">
    <MyDatePicker />
    <DayRecordForm class="flex-1" :transactions="records[currentDate] || []" :date="currentDate" />
  </main>
</template>
