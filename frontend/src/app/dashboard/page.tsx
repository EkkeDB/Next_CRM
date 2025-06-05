import type { Metadata } from 'next'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { DashboardStats } from '@/components/dashboard/dashboard-stats'
import { RevenueChart } from '@/components/dashboard/revenue-chart'
import { ContractsChart } from '@/components/dashboard/contracts-chart'
import { StatusDistributionChart } from '@/components/dashboard/status-distribution'
import { UpcomingDeliveries } from '@/components/dashboard/upcoming-deliveries'
import { TopCommodities } from '@/components/dashboard/top-commodities'
import { DashboardContent } from './dashboard-content'

export const metadata: Metadata = {
  title: 'Dashboard',
  description: 'NextCRM Dashboard - Overview of your commodity trading portfolio',
}

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">
            Welcome to your commodity trading overview
          </p>
        </div>

        {/* Dashboard Content */}
        <DashboardContent />
      </div>
    </DashboardLayout>
  )
}