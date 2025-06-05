import type { Metadata } from 'next'
import { DashboardLayout } from '@/components/layout/dashboard-layout'

export const metadata: Metadata = {
  title: 'Counterparties',
  description: 'Manage your trading counterparties',
}

export default function CounterpartiesPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Counterparties</h1>
          <p className="text-gray-600 mt-2">
            Manage your trading counterparties and business relationships
          </p>
        </div>

        {/* Placeholder for counterparties content */}
        <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Counterparties Management
          </h3>
          <p className="text-gray-600 mb-4">
            This section is under development. You can manage your trading counterparties here.
          </p>
          <div className="text-sm text-gray-500">
            Coming soon: Create, edit, and manage counterparty relationships
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}