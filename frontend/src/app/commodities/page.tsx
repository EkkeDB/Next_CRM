import type { Metadata } from 'next'
import { DashboardLayout } from '@/components/layout/dashboard-layout'

export const metadata: Metadata = {
  title: 'Commodities',
  description: 'Manage commodity types and specifications',
}

export default function CommoditiesPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Commodities</h1>
          <p className="text-gray-600 mt-2">
            Manage commodity types, groups, and specifications
          </p>
        </div>

        {/* Placeholder for commodities content */}
        <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Commodities Management
          </h3>
          <p className="text-gray-600 mb-4">
            This section is under development. You can manage your commodity catalog here.
          </p>
          <div className="text-sm text-gray-500">
            Coming soon: Commodity groups, types, and quality specifications
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}