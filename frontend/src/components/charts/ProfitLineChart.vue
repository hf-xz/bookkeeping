<script lang="ts" setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import type { ProfitResponse } from '@/apis/transactions'
import { localeDateString } from '@/utils/date'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

const props = defineProps<{
  profitData: ProfitResponse[]
}>()

const chartData = computed(() => {
  const labels = props.profitData.map((p) => localeDateString(p.record_date))
  const data = props.profitData.map((p) => p.profit)

  return {
    labels,
    datasets: [
      {
        label: '利润',
        data,
        borderColor: '#18a058',
        backgroundColor: 'rgba(24, 160, 88, 0.1)',
        fill: true,
        tension: 0.3,
      },
    ],
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    x: {
      display: false,
    },
  },
}
</script>

<template>
  <div class="h-40">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>
