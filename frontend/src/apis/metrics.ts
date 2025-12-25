// transactions.ts
// API related to transactions

export const readMetrics = async () => {
  return await request('/metrics', {
    method: 'GET',
  }).then((data) => data as Metric[])
}
