<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import type { Metric, MetricType } from '@/models/metric'
import { readMetrics, createMetric, updateMetric, deleteMetric } from '@/apis/metrics'
import { showConfirmDialog, showToast } from 'vant'

const loading = ref(false)
const metrics = ref<Metric[]>([])
const showEditPopup = ref(false)
const editingMetric = ref<Partial<Metric>>({})
const isEditing = ref(false)

const typeOptions = [
  { text: '每日', value: 'daily' },
  { text: '可选', value: 'optional' },
]

// 加载指标列表
const loadMetrics = async () => {
  loading.value = true
  try {
    metrics.value = await readMetrics()
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadMetrics()
})

// 新建
const onAdd = () => {
  editingMetric.value = {
    name: '',
    unit: '',
    weight: 1.0,
    type: 'optional',
    description: '',
    is_active: true,
  }
  isEditing.value = false
  showEditPopup.value = true
}

// 编辑
const onEdit = (metric: Metric) => {
  editingMetric.value = { ...metric }
  isEditing.value = true
  showEditPopup.value = true
}

// 保存
const onSave = async () => {
  if (!editingMetric.value.name) {
    showToast('请输入指标名称')
    return
  }
  try {
    if (isEditing.value && editingMetric.value.id) {
      await updateMetric(editingMetric.value.id, editingMetric.value)
      showToast('更新成功')
    } else {
      await createMetric(editingMetric.value as Omit<Metric, 'id'>)
      showToast('创建成功')
    }
    showEditPopup.value = false
    loadMetrics()
  } catch (e) {
    showToast('操作失败')
  }
}

// 删除
const onDelete = async (id: number) => {
  try {
    await showConfirmDialog({
      title: '确认删除',
      message: '删除后相关记录也会被删除，确认删除？',
    })
    await deleteMetric(id)
    showToast('删除成功')
    loadMetrics()
  } catch (e) {
    // 用户取消
  }
}
</script>

<template>
  <main class="h-full flex flex-col p-4 gap-4">
    <van-pull-refresh v-model="loading" @refresh="loadMetrics">
      <van-cell-group inset>
        <van-cell
          v-for="metric in metrics"
          :key="metric.id"
          :title="metric.name"
          :label="`单位: ${metric.unit || '-'} | 类型: ${metric.type || '-'}`"
          is-link
          @click="onEdit(metric)"
        >
          <template #value>
            <van-tag :type="metric.is_active ? 'success' : 'default'">
              {{ metric.is_active ? '启用' : '禁用' }}
            </van-tag>
          </template>
        </van-cell>
      </van-cell-group>
    </van-pull-refresh>

    <van-button type="primary" block round @click="onAdd">新增指标</van-button>

    <van-popup v-model:show="showEditPopup" position="bottom" round :style="{ height: '70%' }">
      <div class="p-4 flex flex-col gap-4 h-full">
        <div class="text-lg font-bold">{{ isEditing ? '编辑指标' : '新增指标' }}</div>

        <van-cell-group>
          <van-field v-model="editingMetric.name!" label="名称" placeholder="如：销售额" required />
          <van-field v-model="editingMetric.unit!" label="单位" placeholder="如：元、人" />
          <van-field
            v-model.number="editingMetric.weight!"
            type="number"
            label="权重"
            placeholder="1.0"
          />
          <van-radio-group v-model="editingMetric.type!" direction="horizontal" class="ml-2">
            <van-radio name="daily">每日</van-radio>
            <van-radio name="optional">可选</van-radio>
          </van-radio-group>
          <van-field v-model="editingMetric.description!" label="描述" placeholder="可选" />
          <van-cell center title="启用">
            <template #value>
              <van-switch v-model="editingMetric.is_active!" />
            </template>
          </van-cell>
        </van-cell-group>

        <div class="flex gap-2 mt-auto">
          <van-button v-if="isEditing" type="danger" block @click="onDelete(editingMetric.id!)">
            删除
          </van-button>
          <van-button type="primary" block @click="onSave">保存</van-button>
        </div>
      </div>
    </van-popup>
  </main>
</template>
