// transactions.ts
// API related to transactions
import { API_BASE } from './index'

const url = `${API_BASE}/metrics`

export const readMetrics = async () => {
  console.log('Fetching metrics from:', url)

  return await fetch(url, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  })
    .then((res) => res.json())
    .then((data) => data as Metric[])
}
