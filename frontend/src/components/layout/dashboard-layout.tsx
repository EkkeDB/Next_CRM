'use client'

import { useState } from 'react'
import { Sidebar, SidebarToggle } from './sidebar'
import { AuthGuard } from '@/components/auth/auth-guard'

interface DashboardLayoutProps {
  children: React.ReactNode
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50">
        <Sidebar 
          isOpen={sidebarOpen} 
          onClose={() => setSidebarOpen(false)} 
        />
        
        <div className="lg:pl-64">
          {/* Top bar */}
          <div className="sticky top-0 z-10 bg-white border-b border-gray-200 px-4 py-4 lg:px-6">
            <div className="flex items-center gap-4">
              <SidebarToggle onClick={() => setSidebarOpen(true)} />
              <div className="flex-1">
                {/* You can add search bar or other top bar content here */}
              </div>
            </div>
          </div>

          {/* Main content */}
          <main className="p-4 lg:p-6">
            {children}
          </main>
        </div>
      </div>
    </AuthGuard>
  )
}