// transactions.ts
// API related to transactions

export const readTransactions = async (
  start_date?: string,
  end_date?: string,
  metric_id?: number,
) => {
  const params = new URLSearchParams()
  if (start_date) params.append('start_date', start_date)
  if (end_date) params.append('end_date', end_date)
  if (metric_id) params.append('metric_id', metric_id.toString())

  const queryString = params.toString ? '?' + params.toString() : ''

  return await request('transactions' + queryString, {
    method: 'GET',
  }).then((data) => data as TransactionWithMetricName[])
}

export const readOnedayTransactions = async (date: string) => {
  return await readTransactions(date, date)
}

export const readTodayTransactions = async () => {
  const todayStr = getTodayStr()
  return await readOnedayTransactions(todayStr)
}

export const upsertTransactions = async (transaction: TransactionUpsert) => {
  return await request('/transactions', {
    method: 'POST',
    body: JSON.stringify(transaction),
  })
}

export const bulkUpsertTransactions = async (transactions: TransactionUpsert[]) => {
  return await request('/transactions/bulk', {
    method: 'POST',
    body: JSON.stringify(transactions),
  })
}
