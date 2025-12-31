<script lang="ts" setup>
const props = defineProps<{
  formEditing: boolean
  transactions: Array<TransactionWithMetricName>
  date: string
}>()

// Metrics 列表
const metrics = ref<Metric[]>()

// 表单相关
const formData = ref<Record<string, string>>({}) // key: metric_id, value: input value
const submiting = ref(false)
const editing = computed({
  get: () => props.formEditing,
  set: (val: boolean) => {
    emit('update:formEditing', val)
  },
})

const onSubmit = () => {
  console.log('提交记录表单', formData.value)
  submiting.value = true
  const toUpsert: TransactionUpsert[] = []
  for (const metricName in formData.value) {
    const metricId = metrics.value?.find((m) => m.name === metricName)?.id
    if (!metricId) {
      console.warn(`未知的指标名称: ${metricName}，跳过`)
      continue
    }
    toUpsert.push({
      metric_id: metricId,
      record_date: props.date,
      value: parseFloat(formData.value[metricName]!),
      note: '',
    })
  }
  bulkUpsertTransactions(toUpsert)
    .then(() => {
      editing.value = false
    })
    .finally(() => {
      submiting.value = false
    })
}

// 加载已有记录到表单
const loadExistingRecord = async () => {
  for (const txn of props.transactions) {
    formData.value[txn.metric_name] = txn.value.toString()
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
onMounted(async () => {
  // 加载指标列表
  metrics.value = await readMetrics()
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
          v-model="formData[metric.name]"
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
