export interface Metric {
  id: number
  name: string
  unit: string
  weight: number
  fixed: boolean
  description: string
  is_active: boolean
}
