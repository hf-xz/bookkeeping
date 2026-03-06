<script lang="ts" setup>
import { ref, computed } from 'vue'
import { onActivated } from 'vue'
import { readMetrics } from '@/apis/metrics'
import { readOnedayTransactions, readProfit, type ProfitResponse } from '@/apis/transactions'
import { getToday } from '@/utils/date'

const today = getToday()
const metrics = ref<Metric[]>([])
const todayTransactions = ref<TransactionWithMetricName[]>([])
const todayProfit = ref<ProfitResponse | null>(null)

// 今日填写情况
const filledMetrics = computed(() => {
  return todayTransactions.value.map((t) => t.metric_name)
})

const filledCount = computed(() => filledMetrics.value.length)
const totalCount = computed(() => metrics.value.length)
const fillRate = computed(() => {
  if (totalCount.value === 0) return 0
  return Math.round((filledCount.value / totalCount.value) * 100)
})

// 加载数据
const loadData = async () => {
  // 并行请求
  const [metricsRes, txnsRes, profitRes] = await Promise.all([
    readMetrics(),
    readOnedayTransactions(today),
    readProfit(today, today),
  ])

  metrics.value = metricsRes
  todayTransactions.value = txnsRes
  todayProfit.value = profitRes[0] || null
}

// 每次页面显示时刷新
onActivated(() => {
  loadData()
})
</script>

<template>
  <main class="h-full flex flex-col p-4 gap-4 overflow-y-auto">
    <!-- 今日概览 -->
    <div class="text-lg font-bold">今日概览</div>

    <van-cell-group inset>
      <van-cell title="填写进度">
        <template #value>
          <span :class="fillRate === 100 ? 'text-green-500' : 'text-orange-500'">
            {{ filledCount }} / {{ totalCount }} ({{ fillRate }}%)
          </span>
        </template>
      </van-cell>
      <van-cell title="今日利润">
        <template #value>
          <span
            :class="todayProfit && todayProfit.profit >= 0 ? 'text-green-500' : 'text-red-500'"
          >
            {{ todayProfit?.profit?.toFixed(2) ?? '--' }} 元
          </span>
        </template>
      </van-cell>
    </van-cell-group>
  </main>
</template>
