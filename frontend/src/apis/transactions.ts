// transactions.ts
// API related to transactions
import { API_BASE } from './index'

const url = `${API_BASE}/transactions`

export const readTransactions = async (
  start_date?: string,
  end_date?: string,
  metric_id?: number,
) => {
  const params = new URLSearchParams()
  if (start_date) params.append('start_date', start_date)
  if (end_date) params.append('end_date', end_date)
  if (metric_id) params.append('metric_id', metric_id.toString())

  const queryString = params.toString()
  const fullUrl = queryString ? `${url}?${queryString}` : url

  console.log('Fetching transactions from:', fullUrl)

  return await fetch(fullUrl, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  })
    .then((res) => res.json())
    .then((data) => data as TransactionWithMetricName[])
}

export const readOnedayTransactions = async (date: string) => {
  return await readTransactions(date, date)
}

export const readTodayTransactions = async () => {
  const todayStr = getTodayStr()
  return await readOnedayTransactions(todayStr)
}
