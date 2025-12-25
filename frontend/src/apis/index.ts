export const API_BASE = import.meta.env.VITE_API_BASE || '/api'

export const request = async (endpoint: string, options: RequestInit = {}) => {
  console.log(`Requesting ${endpoint} with options:`, options)
  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    console.error(`API request to ${endpoint} failed with status ${res.status}`)
    throw new Error(`API request failed with status ${res.status}`)
  }
  return res.json()
}
