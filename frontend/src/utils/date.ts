// utils/date.ts
import type { Dayjs } from 'dayjs'
import dayjs from 'dayjs'

dayjs.locale('zh-cn')

const DATE_FORMAT = 'YYYY-MM-DD'
const ZH_DATE_FORMAT = 'YYYY年 MM月 DD日'

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

export const localeDateString = (dateStr: string): string => {
  return dayjs(dateStr).format(ZH_DATE_FORMAT)
}

// 获取本月第一天和最后一天
export const getCurrentMonthRange = (): { start: string; end: string } => {
  const start = dayjs().startOf('month').format(DATE_FORMAT)
  const end = dayjs().endOf('month').format(DATE_FORMAT)
  return { start, end }
}

// 获取上月第一天和最后一天
export const getLastMonthRange = (): { start: string; end: string } => {
  const start = dayjs().subtract(1, 'month').startOf('month').format(DATE_FORMAT)
  const end = dayjs().subtract(1, 'month').endOf('month').format(DATE_FORMAT)
  return { start, end }
}
