'use client'

import { DashboardStats } from '@/components/dashboard/dashboard-stats'
import { RevenueChart } from '@/components/dashboard/revenue-chart'
import { ContractsChart } from '@/components/dashboard/contracts-chart'
import { StatusDistributionChart } from '@/components/dashboard/status-distribution'
import { UpcomingDeliveries } from '@/components/dashboard/upcoming-deliveries'
import { TopCommodities } from '@/components/dashboard/top-commodities'
import { useDashboardStats } from '@/hooks/use-dashboard'

export function DashboardContent() {
  const { data: stats, isLoading, error } = useDashboardStats()

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">
          <svg
            className="mx-auto h-12 w-12"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
            />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          Unable to load dashboard data
        </h3>
        <p className="text-gray-600">
          Please check your connection and try refreshing the page.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Stats Overview */}
      <DashboardStats />

      {/* Charts Grid */}
      <div className="grid gap-6 lg:grid-cols-2">
        <RevenueChart 
          data={stats?.monthly_revenue || []} 
          isLoading={isLoading} 
        />
        <ContractsChart 
          data={stats?.monthly_contracts || []} 
          isLoading={isLoading} 
        />
      </div>

      {/* Second Row */}
      <div className="grid gap-6 lg:grid-cols-3">
        <StatusDistributionChart 
          data={stats?.status_distribution || {}} 
          isLoading={isLoading} 
        />
        <TopCommodities 
          data={stats?.top_commodities || []} 
          isLoading={isLoading} 
        />
        <UpcomingDeliveries 
          data={stats?.upcoming_deliveries || []} 
          isLoading={isLoading} 
        />
      </div>
    </div>
  )
}