export interface Transaction {
  id: number
  metric_id: number
  value: number
  record_date: string
  note: string
}

export type TransactionUpsert = Omit<Transaction, 'id'>

export interface TransactionWithMetricName extends Transaction {
  metric_name: string
}
