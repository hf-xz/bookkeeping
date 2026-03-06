<script lang="ts" setup>
import { computed } from 'vue'
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import type { ProfitResponse } from '@/apis/transactions'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps<{
  profitData: ProfitResponse[]
}>()

const chartData = computed(() => {
  // 聚合所有指标在各天的利润贡献
  const detailMap = new Map<string, number>()

  for (const p of props.profitData) {
    for (const [metricName, value] of Object.entries(p.details)) {
      const current = detailMap.get(metricName) || 0
      detailMap.set(metricName, current + value)
    }
  }

  const labels = Array.from(detailMap.keys())
  const data = Array.from(detailMap.values())

  return {
    labels,
    datasets: [
      {
        data,
        backgroundColor: [
          '#18a058',
          '#fbbd23',
          '#1989fa',
          '#ee0a24',
          '#7238c1',
          '#f85959',
          '#5cdbd3',
          '#ff9d00',
        ],
      },
    ],
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right' as const,
      labels: {
        boxWidth: 12,
        font: {
          size: 12,
        },
      },
    },
  },
}
</script>

<template>
  <div class="h-40">
    <Pie :data="chartData" :options="chartOptions" />
  </div>
</template>
