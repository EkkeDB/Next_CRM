import type { Metadata } from 'next'
import { DashboardLayout } from '@/components/layout/dashboard-layout'

export const metadata: Metadata = {
  title: 'Settings',
  description: 'Application settings and preferences',
}

export default function SettingsPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="text-gray-600 mt-2">
            Manage your account settings and application preferences
          </p>
        </div>

        {/* Placeholder for settings content */}
        <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Settings & Preferences
          </h3>
          <p className="text-gray-600 mb-4">
            This section is under development. You can configure your application here.
          </p>
          <div className="text-sm text-gray-500">
            Coming soon: User preferences, notifications, and system configuration
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}