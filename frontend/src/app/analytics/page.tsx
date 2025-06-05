import type { Metadata } from 'next'
import { DashboardLayout } from '@/components/layout/dashboard-layout'

export const metadata: Metadata = {
  title: 'Analytics',
  description: 'Advanced analytics and reporting',
}

export default function AnalyticsPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
          <p className="text-gray-600 mt-2">
            Advanced analytics and reporting for your trading portfolio
          </p>
        </div>

        {/* Placeholder for analytics content */}
        <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Advanced Analytics
          </h3>
          <p className="text-gray-600 mb-4">
            This section is under development. You'll find detailed analytics and reports here.
          </p>
          <div className="text-sm text-gray-500">
            Coming soon: Performance reports, risk analysis, and market insights
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}