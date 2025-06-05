import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import apiClient from './api'
import type { UserProfile, LoginCredentials, RegisterData } from '@/types'

interface AuthState {
  user: UserProfile | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (credentials: LoginCredentials) => Promise<void>
  register: (data: RegisterData) => Promise<void>
  logout: () => Promise<void>
  updateProfile: (data: Partial<UserProfile>) => Promise<void>
  checkAuth: () => Promise<void>
  clearAuth: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (credentials: LoginCredentials) => {
        try {
          set({ isLoading: true })
          
          await apiClient.login(credentials)
          
          // Get user profile after successful login
          const profile = await apiClient.getProfile()
          
          set({
            user: profile,
            isAuthenticated: true,
            isLoading: false,
          })
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      register: async (data: RegisterData) => {
        try {
          set({ isLoading: true })
          
          await apiClient.register(data)
          
          // Auto-login after registration
          await get().login({
            username: data.username,
            password: data.password,
          })
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      logout: async () => {
        try {
          await apiClient.logout()
        } catch (error) {
          // Continue with logout even if API call fails
          console.error('Logout error:', error)
        } finally {
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
          })
        }
      },

      updateProfile: async (data: Partial<UserProfile>) => {
        try {
          const updatedProfile = await apiClient.updateProfile(data)
          set({ user: updatedProfile })
        } catch (error) {
          throw error
        }
      },

      checkAuth: async () => {
        try {
          set({ isLoading: true })
          
          const profile = await apiClient.getProfile()
          
          set({
            user: profile,
            isAuthenticated: true,
            isLoading: false,
          })
        } catch (error) {
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
          })
        }
      },

      clearAuth: () => {
        set({
          user: null,
          isAuthenticated: false,
          isLoading: false,
        })
      },
    }),
    {
      name: 'nextcrm-auth',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)

// Auth helper functions
export const getAuthState = () => useAuthStore.getState()

export const isAuthenticated = () => {
  const { isAuthenticated } = getAuthState()
  return isAuthenticated
}

export const getUser = () => {
  const { user } = getAuthState()
  return user
}

export const requireAuth = () => {
  const { isAuthenticated, user } = getAuthState()
  if (!isAuthenticated || !user) {
    throw new Error('Authentication required')
  }
  return user
}

// Route protection helper
export const withAuth = <T extends Record<string, any>>(
  WrappedComponent: React.ComponentType<T>
) => {
  const AuthenticatedComponent = (props: T) => {
    const { isAuthenticated, checkAuth } = useAuthStore()
    
    React.useEffect(() => {
      if (!isAuthenticated) {
        checkAuth()
      }
    }, [isAuthenticated, checkAuth])

    if (!isAuthenticated) {
      // You can return a loading spinner or redirect here
      return null
    }

    return <WrappedComponent {...props} />
  }

  AuthenticatedComponent.displayName = `withAuth(${WrappedComponent.displayName || WrappedComponent.name})`
  
  return AuthenticatedComponent
}