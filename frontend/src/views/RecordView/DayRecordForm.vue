<script lang="ts" setup>
const props = defineProps<{
  transactions: Array<TransactionWithMetricName>
}>()

// Metrics 列表
const metrics = ref<Metric[]>()

// 表单相关
const formData = ref<Record<string, number>>({}) // key: metric_id, value: input value

const onSubmit = () => {
  console.log('提交记录表单')
}

// 初始化
onMounted(async () => {
  // 加载指标列表
  metrics.value = await readMetrics()
})
</script>

<template>
  <van-form @submit="onSubmit" class="mt-4 flex flex-col gap-4">
    <h2 class="text-2xl font-bold">每日记录</h2>
    <van-cell-group>
      <van-field
        v-for="metric in metrics"
        v-model="formData[metric.name]"
        :label="metric.name"
        :placeholder="metric.unit"
        type="number"
      >
        {{ metric.name }}
      </van-field>
    </van-cell-group>
    <div class="mx-4">
      <van-button round block type="primary" native-type="submit"> 提交 </van-button>
    </div>
  </van-form>
</template>
