import type { Metadata } from 'next'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { ContractsTable } from '@/components/contracts/contracts-table'

export const metadata: Metadata = {
  title: 'Contracts',
  description: 'Manage your commodity trading contracts',
}

export default function ContractsPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Contracts</h1>
          <p className="text-gray-600 mt-2">
            Manage your commodity trading contracts
          </p>
        </div>

        {/* Contracts Table */}
        <ContractsTable />
      </div>
    </DashboardLayout>
  )
}