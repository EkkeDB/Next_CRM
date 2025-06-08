'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/auth'
import { debouncedNavigate, canNavigate } from '@/lib/navigation-utils'

export default function HomePage() {
  const router = useRouter()
  const { isAuthenticated, isLoading } = useAuthStore()

  useEffect(() => {
    // Only redirect after we know the auth status
    if (!isLoading && canNavigate()) {
      if (isAuthenticated) {
        debouncedNavigate(router, '/dashboard', true, 300)
      } else {
        debouncedNavigate(router, '/login', true, 300)
      }
    }
  }, [isAuthenticated, isLoading, router])

  // Show loading while determining where to redirect
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="flex flex-col items-center gap-4">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
        <p className="text-sm text-gray-600">Loading NextCRM...</p>
      </div>
    </div>
  )
}