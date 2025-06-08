'use client'

import { useEffect, useRef, useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { useAuthStore } from '@/lib/auth'
import { debouncedNavigate, canNavigate } from '@/lib/navigation-utils'

interface AuthGuardProps {
  children: React.ReactNode
  requireAuth?: boolean
  redirectTo?: string
}

export function AuthGuard({ 
  children, 
  requireAuth = true, 
  redirectTo = '/login' 
}: AuthGuardProps) {
  const router = useRouter()
  const pathname = usePathname()
  const { isAuthenticated, isLoading, checkAuth } = useAuthStore()
  
  // Prevent multiple authentication checks and redirects
  const hasCheckedAuth = useRef(false)
  const hasRedirected = useRef(false)
  const [isInitialized, setIsInitialized] = useState(false)

  // Check authentication once on mount
  useEffect(() => {
    if (!hasCheckedAuth.current && !isAuthenticated && !isLoading) {
      hasCheckedAuth.current = true
      checkAuth().finally(() => {
        setIsInitialized(true)
      })
    } else if (isAuthenticated || (!isAuthenticated && isLoading === false)) {
      // If we already have auth status, mark as initialized
      setIsInitialized(true)
    }
  }, []) // Empty dependency array - only run once on mount

  // Handle navigation based on auth status
  useEffect(() => {
    // Only navigate after auth check is complete and we haven't redirected yet
    if (isInitialized && !hasRedirected.current && !isLoading && canNavigate()) {
      if (requireAuth && !isAuthenticated) {
        hasRedirected.current = true
        // Store the current path to redirect back after login
        const returnUrl = pathname !== '/login' && pathname !== '/register' 
          ? `?returnUrl=${encodeURIComponent(pathname)}` 
          : ''
        const targetPath = `${redirectTo}${returnUrl}`
        debouncedNavigate(router, targetPath, true, 200)
      } else if (!requireAuth && isAuthenticated) {
        hasRedirected.current = true
        // If user is authenticated but shouldn't be (like on login page), redirect to dashboard
        debouncedNavigate(router, '/dashboard', true, 200)
      }
    }
  }, [isAuthenticated, isLoading, isInitialized, requireAuth, pathname, redirectTo, router])

  // Reset redirect flag when pathname changes (user navigated manually)
  useEffect(() => {
    hasRedirected.current = false
  }, [pathname])

  // Show loading state while checking authentication
  if (!isInitialized || isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
          <p className="text-sm text-gray-600">Checking authentication...</p>
        </div>
      </div>
    )
  }

  // Don't render children if auth requirements aren't met and we're about to redirect
  if (requireAuth && !isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
          <p className="text-sm text-gray-600">Redirecting to login...</p>
        </div>
      </div>
    )
  }

  if (!requireAuth && isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
          <p className="text-sm text-gray-600">Redirecting to dashboard...</p>
        </div>
      </div>
    )
  }

  return <>{children}</>
}

// Higher-order component for protecting pages
export function withAuthGuard<P extends object>(
  Component: React.ComponentType<P>,
  options?: { requireAuth?: boolean; redirectTo?: string }
) {
  const WrappedComponent = (props: P) => {
    return (
      <AuthGuard requireAuth={options?.requireAuth} redirectTo={options?.redirectTo}>
        <Component {...props} />
      </AuthGuard>
    )
  }

  WrappedComponent.displayName = `withAuthGuard(${Component.displayName || Component.name})`
  
  return WrappedComponent
}