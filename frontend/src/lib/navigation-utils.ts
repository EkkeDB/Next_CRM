import { AppRouterInstance } from 'next/dist/shared/lib/app-router-context.shared-runtime'

/**
 * Safe navigation wrapper that handles antivirus software interference
 * and other navigation issues
 */
export function safeNavigate(router: AppRouterInstance, path: string, replace = false) {
  try {
    if (replace) {
      router.replace(path)
    } else {
      router.push(path)
    }
  } catch (error) {
    // Handle antivirus software blocking navigation
    if (error instanceof DOMException && error.message.includes('insecure')) {
      console.warn('Navigation blocked by security software, retrying with window.location')
      try {
        if (replace) {
          window.location.replace(path)
        } else {
          window.location.href = path
        }
      } catch (fallbackError) {
        console.error('All navigation methods failed:', fallbackError)
      }
    } else {
      console.error('Navigation error:', error)
      // Fallback to window.location for other errors
      try {
        if (replace) {
          window.location.replace(path)
        } else {
          window.location.href = path
        }
      } catch (fallbackError) {
        console.error('Fallback navigation failed:', fallbackError)
      }
    }
  }
}

/**
 * Debounced navigation to prevent "too many calls" errors
 */
const navigationTimeouts = new Map<string, NodeJS.Timeout>()

export function debouncedNavigate(
  router: AppRouterInstance, 
  path: string, 
  replace = false, 
  delay = 100
) {
  const key = `${path}-${replace}`
  
  // Clear any pending navigation to the same path
  const existingTimeout = navigationTimeouts.get(key)
  if (existingTimeout) {
    clearTimeout(existingTimeout)
  }
  
  // Schedule new navigation
  const timeout = setTimeout(() => {
    safeNavigate(router, path, replace)
    navigationTimeouts.delete(key)
  }, delay)
  
  navigationTimeouts.set(key, timeout)
}

/**
 * Check if we're in a browser environment and navigation is available
 */
export function canNavigate(): boolean {
  return typeof window !== 'undefined' && typeof window.history !== 'undefined'
}