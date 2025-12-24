<!-- RecordView  -->
<script lang="ts" setup>
interface DayRecord {
  date: string
  transactions: Array<Omit<TransactionWithMetricName, 'record_date'>>
}
const records = ref<DayRecord[]>([]) // 所有日期的记录缓存列表

const today = getToday()

const currentDate = ref<string>(getToday())

const transactions2records = (transactions: TransactionWithMetricName[]) => {
  const recordMap: Record<string, DayRecord> = {}
  transactions.forEach((tx) => {
    if (!recordMap[tx.record_date]) {
      recordMap[tx.record_date] = {
        date: tx.record_date,
        transactions: [],
      }
    }
    const { record_date, ...rest } = tx
    recordMap[tx.record_date]!.transactions.push(rest)
  })
  return Object.values(recordMap)
}

const mergeRecords = (newRecords: DayRecord[]) => {
  newRecords.forEach((newRecord) => {
    const existingIndex = records.value.findIndex((record) => record.date === newRecord.date)
    if (existingIndex !== -1) {
      // 替换已有记录
      records.value[existingIndex] = newRecord
    } else {
      // 添加新记录
      records.value.push(newRecord)
    }
  })
  // 按日期降序排序
  records.value.sort((a, b) => (a.date < b.date ? 1 : -1))
}

onMounted(async () => {
  // 初始加载最近一周的记录
  const startDate = addDate(today, -6)
  const res = await readTransactions(startDate, today)
  const dayRecords = transactions2records(res)
  mergeRecords(dayRecords)
})
</script>

<template>
  <h1 class="text-3xl font-bold text-blue-600">记录</h1>
  <div v-for="record in records" :key="record.date">
    <h2 class="text-2xl font-semibold mt-4 mb-2">
      {{ record.date }}
    </h2>
    <div v-for="txn in record.transactions" :key="txn.id">
      {{ `${txn.metric_name}: ${txn.value}` }}
    </div>
  </div>
</template>
