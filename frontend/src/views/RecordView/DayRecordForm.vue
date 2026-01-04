<script lang="ts" setup>
const props = defineProps<{
  formEditing: boolean
  transactions: Array<TransactionWithMetricName>
  date: string
}>()

// Metrics 列表
const metrics = ref<Metric[]>()

// 表单相关
const formData = ref<Record<string, number>>({}) // key: metric_id, value: input value
const submiting = ref(false)
const editing = computed({
  get: () => props.formEditing,
  set: (val: boolean) => {
    emit('update:formEditing', val)
  },
})

// 提交表单
const onSubmit = () => {
  console.log('提交记录表单', formData.value)
  submiting.value = true
  const toUpsert: TransactionUpsert[] = []
  // 遍历表单数据
  for (const metricName in formData.value) {
    // 查找对应的 metric_id
    const metricId = metrics.value?.find((m) => m.name === metricName)?.id
    if (!metricId) {
      console.warn(`未知的指标名称: ${metricName}，跳过`)
      continue
    }
    // 如果没有填写值，跳过
    if (!formData.value[metricName]) {
      continue
    }
    // 如果与原有记录相同，跳过
    const existingTxn = props.transactions.find((t) => t.metric_name === metricName)
    if (existingTxn && existingTxn.value === formData.value[metricName]) {
      continue
    }
    // 准备 upsert 数据
    toUpsert.push({
      metric_id: metricId,
      record_date: props.date,
      value: formData.value[metricName],
      note: '',
    })
  }
  // 如果没有需要 upsert 的数据，直接返回
  if (toUpsert.length === 0) {
    submiting.value = false
    editing.value = false
    loadExistingRecord()
    return
  }
  // 执行批量 upsert
  bulkUpsertTransactions(toUpsert)
    .then(() => {
      editing.value = false
      emit('upsertSuccess')
    })
    .finally(() => {
      submiting.value = false
    })
}

// 加载已有记录到表单
const loadExistingRecord = async () => {
  formData.value = {}
  for (const txn of props.transactions) {
    formData.value[txn.metric_name] = txn.value
  }
}

const startEdit = () => {
  editing.value = true
}
const canclelEdit = () => {
  editing.value = false
  formData.value = {}
  loadExistingRecord()
}

// 初始化
onMounted(() => {
  // 加载指标列表
  readMetrics().then((res) => {
    metrics.value = res
  })
  // 加载已有记录
  watch(
    () => props.transactions,
    () => {
      loadExistingRecord()
    },
    { immediate: true },
  )
})

// 定义事件
const emit = defineEmits<{
  (e: 'update:formEditing', value: boolean): void
  (e: 'upsertSuccess'): void
}>()
</script>

<template>
  <van-form
    @submit="onSubmit"
    :readonly="!editing"
    :disabled="submiting"
    class="relative h-full overflow-hidden"
  >
    <div class="pb-16 h-full overflow-y-auto">
      <van-cell-group>
        <van-field
          v-for="metric in metrics"
          v-model.number="formData[metric.name]"
          :label="`${metric.name}${metric.unit ? ` (${metric.unit})` : ''}`"
          label-width="8em"
          :placeholder="metric.description || '0'"
          type="number"
        >
          {{ metric.name }}
        </van-field>
      </van-cell-group>
    </div>

    <div class="absolute bottom-2 right-2 flex gap-2 justify-end">
      <template v-if="!editing">
        <van-button round type="primary" icon="edit" class="shadow-md" @click="startEdit">
          编辑
        </van-button>
      </template>
      <template v-else>
        <van-button round type="success" icon="success" class="shadow-md" native-type="submit">
          保存
        </van-button>
        <van-button round type="primary" icon="cross" class="shadow-md" @click="canclelEdit">
          取消
        </van-button>
      </template>
    </div>
  </van-form>
</template>
