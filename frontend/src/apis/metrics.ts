// metrics.ts
// API related to metrics

import { request } from './index'

export const readMetrics = async () => {
  return await request('/metrics', {
    method: 'GET',
  }).then((data) => data as Metric[])
}

export const createMetric = async (metric: Omit<Metric, 'id'>) => {
  return await request('/metrics', {
    method: 'POST',
    body: JSON.stringify(metric),
  }).then((data) => data as Metric)
}

export const updateMetric = async (id: number, metric: Partial<Metric>) => {
  return await request(`/metrics/${id}`, {
    method: 'PUT',
    body: JSON.stringify(metric),
  }).then((data) => data as Metric)
}

export const deleteMetric = async (id: number) => {
  return await request(`/metrics/${id}`, {
    method: 'DELETE',
  })
}
