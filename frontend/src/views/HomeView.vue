<script lang="ts" setup>
import { ref, computed } from 'vue'
import { onActivated } from 'vue'
import { readMetrics } from '@/apis/metrics'
import { readOnedayTransactions, readProfit, type ProfitResponse } from '@/apis/transactions'
import { getToday, getCurrentMonthRange } from '@/utils/date'
import ProfitLineChart from '@/components/charts/ProfitLineChart.vue'
import ProfitPieChart from '@/components/charts/ProfitPieChart.vue'

const today = getToday()
const metrics = ref<Metric[]>([])
const todayTransactions = ref<TransactionWithMetricName[]>([])
const todayProfit = ref<ProfitResponse | null>(null)
const monthProfitData = ref<ProfitResponse[]>([])

// 只统计每日类型的指标
const dailyMetrics = computed(() => metrics.value.filter((m) => m.type === 'daily'))

// 今日填写情况（只统计每日指标）
const filledMetrics = computed(() => {
  return todayTransactions.value.map((t) => t.metric_name)
})

const filledCount = computed(() => filledMetrics.value.length)
const totalCount = computed(() => dailyMetrics.value.length)
const fillRate = computed(() => {
  if (totalCount.value === 0) return 0
  return Math.round((filledCount.value / totalCount.value) * 100)
})

// 加载数据
const loadData = async () => {
  const [metricsRes, txnsRes, profitRes, monthProfitRes] = await Promise.all([
    readMetrics(),
    readOnedayTransactions(today),
    readProfit(today, today),
    readProfit(getCurrentMonthRange().start, getCurrentMonthRange().end),
  ])

  metrics.value = metricsRes
  todayTransactions.value = txnsRes
  todayProfit.value = profitRes[0] || null
  monthProfitData.value = monthProfitRes
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
          <span :class="todayProfit && todayProfit.profit >= 0 ? 'text-green-500' : 'text-red-500'">
            {{ todayProfit?.profit?.toFixed(2) ?? '--' }} 元
          </span>
        </template>
      </van-cell>
    </van-cell-group>

    <!-- 本月利润走势图 -->
    <div class="text-lg font-bold">本月利润走势</div>

    <van-cell-group inset>
      <van-cell>
        <template #value>
          <ProfitLineChart v-if="monthProfitData.length > 0" :profit-data="monthProfitData" />
          <div v-else class="h-40 flex items-center justify-center text-gray-400">暂无数据</div>
        </template>
      </van-cell>
    </van-cell-group>

    <!-- 本月利润分布 -->
    <div class="text-lg font-bold">本月利润分布</div>

    <van-cell-group inset>
      <van-cell>
        <template #value>
          <ProfitPieChart v-if="monthProfitData.length > 0" :profit-data="monthProfitData" />
          <div v-else class="h-40 flex items-center justify-center text-gray-400">暂无数据</div>
        </template>
      </van-cell>
    </van-cell-group>
  </main>
</template>
