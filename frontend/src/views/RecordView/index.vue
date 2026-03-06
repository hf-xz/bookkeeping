<!-- RecordView  -->
<script lang="ts" setup>
import { watch } from 'vue'
import { onActivated } from 'vue'
import { readMetrics } from '@/apis/metrics'
import type { TransactionWithMetricName } from '@/models/transaction'
import type { Metric } from '@/models/metric'
import DayRecordForm from './DayRecordForm.vue'
import MyDatePicker from './MyDatePicker.vue'

// 所有日期的记录缓存列表
const records = ref<Record<string, Array<TransactionWithMetricName>>>({})
// 指标列表
const metrics = ref<Metric[]>([])

// 必填指标数量
const dailyMetricsCount = computed(() => metrics.value.filter((m) => m.type === 'daily').length)

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

// 检查是否需要自动进入编辑模式
const shouldAutoEdit = (date: string, txns: TransactionWithMetricName[]): boolean => {
  // 只有今天是自动编辑
  if (date !== today) return false
  // 必填指标数量
  const dailyCount = dailyMetricsCount.value
  if (dailyCount === 0) return false
  // 检查必填指标是否填完
  const filledDailyMetrics = txns.map((t) => t.metric_name)
  const filledDailyCount = metrics.value
    .filter((m) => m.type === 'daily')
    .filter((m) => filledDailyMetrics.includes(m.name)).length
  return filledDailyCount < dailyCount
}

// 更新指定日期的记录
const updateDateRecords = async (date: string, autoEdit = false) => {
  const res = await readOnedayTransactions(date)
  updateRecords(res, date, date)
  // 如果没有记录且 autoEdit 为 true，自动进入编辑模式
  if (autoEdit && res.length === 0) {
    formEditing.value = true
  }
}

// 加载最近一周的记录
const loadWeekData = async () => {
  const startDate = addDate(today, -6)
  const res = await readTransactions(startDate, today)
  updateRecords(res, startDate, today)
}

// 每次页面显示时刷新
onActivated(async () => {
  // 先加载指标列表
  metrics.value = await readMetrics()
  await loadWeekData()
  // 如果当前日期没有记录，自动进入编辑模式
  if (shouldAutoEdit(currentDate.value, records.value[currentDate.value] || [])) {
    formEditing.value = true
  }
})

// 监听日期变化
watch(
  () => currentDate.value,
  (newDate) => {
    // 缓存没有才加载，有缓存则检查是否需要自动编辑
    if (!records.value[newDate]) {
      updateDateRecords(newDate, true)
    } else if (shouldAutoEdit(newDate, records.value[newDate])) {
      formEditing.value = true
    }
  },
)
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
