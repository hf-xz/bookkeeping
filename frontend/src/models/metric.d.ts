export type MetricType = 'daily' | 'optional'

export interface Metric {
  id: number
  name: string
  unit: string
  weight: number
  type: MetricType
  description: string
  is_active: boolean
}
