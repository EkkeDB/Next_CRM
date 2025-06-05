'use client'

import { useQuery } from '@tanstack/react-query'
import apiClient from '@/lib/api'
import { QUERY_KEYS } from '@/lib/constants'
import type { DashboardStats } from '@/types'

export function useDashboardStats() {
  return useQuery({
    queryKey: [QUERY_KEYS.DASHBOARD_STATS],
    queryFn: () => apiClient.getDashboardStats(),
    staleTime: 2 * 60 * 1000, // 2 minutes
    refetchInterval: 5 * 60 * 1000, // Refetch every 5 minutes
  })
}