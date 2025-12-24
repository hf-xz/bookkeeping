// utils/date.ts
import type { Dayjs } from 'dayjs'
import dayjs from 'dayjs'

dayjs.locale('zh-cn')

const DATE_FORMAT = 'YYYY-MM-DD'

export const formatDate = (date: Dayjs): string => {
  return dayjs(date).format(DATE_FORMAT)
}

export const parseDate = (dateStr: string): Dayjs => {
  return dayjs(dateStr, DATE_FORMAT)
}

export const getToday = (): string => {
  return dayjs().format(DATE_FORMAT)
}

export const addDate = (dateStr: string, days: number): string => {
  return dayjs(dateStr).add(days, 'day').format(DATE_FORMAT)
}
