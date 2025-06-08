import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { API_URL, API_ENDPOINTS } from './constants'
import type {
  LoginCredentials,
  RegisterData,
  UserProfile,
  ApiResponse,
  Contract,
  Counterparty,
  Commodity,
  Trader,
  Currency,
  DashboardStats,
  GlobalSearchResults,
  ContractFilters,
  ContractFormData
} from '@/types'

class ApiClient {
  private instance: AxiosInstance
  private isRefreshing: boolean = false
  private failedQueue: Array<{
    resolve: (value?: any) => void
    reject: (error?: any) => void
  }> = []

  constructor() {
    this.instance = axios.create({
      baseURL: API_URL,
      withCredentials: true,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.setupInterceptors()
  }

  private setupInterceptors() {
    // Request interceptor
    this.instance.interceptors.request.use(
      (config) => {
        // Add any request modifications here
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // Response interceptor
    this.instance.interceptors.response.use(
      (response) => {
        return response
      },
      async (error) => {
        const originalRequest = error.config
        
        // Handle circuit breaker responses (429)
        if (error.response?.status === 429) {
          console.warn('Circuit breaker active - authentication service temporarily unavailable')
          this.redirectToLogin()
          return Promise.reject(error)
        }
        
        if (error.response?.status === 401 && !originalRequest._retry) {
          // Prevent infinite retry loops
          originalRequest._retry = true
          
          // Skip refresh for refresh token endpoint itself
          if (originalRequest.url?.includes('/token/refresh')) {
            this.redirectToLogin()
            return Promise.reject(error)
          }
          
          // Skip refresh for profile endpoint if we don't have cookies
          // This prevents infinite loops when checking auth status
          if (originalRequest.url?.includes('/profile') && !this.hasCookies()) {
            this.redirectToLogin()
            return Promise.reject(error)
          }
          
          if (this.isRefreshing) {
            // If refresh is in progress, queue this request
            return new Promise((resolve, reject) => {
              this.failedQueue.push({ resolve, reject })
            }).then(() => {
              return this.instance(originalRequest)
            }).catch(err => {
              return Promise.reject(err)
            })
          }
          
          this.isRefreshing = true
          
          try {
            await this.refreshToken()
            this.processQueue(null)
            this.isRefreshing = false
            // Retry the original request
            return this.instance(originalRequest)
          } catch (refreshError: any) {
            this.processQueue(refreshError)
            this.isRefreshing = false
            
            // Check if it's a circuit breaker error
            if (refreshError.response?.data?.code === 'CIRCUIT_BREAKER_OPEN') {
              console.warn('Circuit breaker open - too many failed refresh attempts')
            }
            
            this.redirectToLogin()
            return Promise.reject(refreshError)
          }
        }
        
        return Promise.reject(error)
      }
    )
  }

  private processQueue(error: any) {
    this.failedQueue.forEach(({ resolve, reject }) => {
      if (error) {
        reject(error)
      } else {
        resolve()
      }
    })
    
    this.failedQueue = []
  }

  private hasCookies(): boolean {
    if (typeof window === 'undefined') return false
    
    // Check if we have refresh token cookie
    return document.cookie.includes('refresh_token=')
  }

  private redirectToLogin() {
    if (typeof window !== 'undefined') {
      // Clear any existing tokens/cookies
      document.cookie = 'access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
      document.cookie = 'refresh_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
      
      // Redirect to login page
      window.location.href = '/login'
    }
  }

  // Generic request method
  private async request<T>(config: AxiosRequestConfig): Promise<T> {
    try {
      const response: AxiosResponse<T> = await this.instance(config)
      return response.data
    } catch (error: any) {
      throw this.handleError(error)
    }
  }

  private handleError(error: any) {
    if (error.response?.data) {
      return error.response.data
    }
    if (error.message) {
      return { message: error.message }
    }
    return { message: 'An unexpected error occurred' }
  }

  // Authentication Methods
  async login(credentials: LoginCredentials) {
    return this.request({
      method: 'POST',
      url: API_ENDPOINTS.AUTH.LOGIN,
      data: credentials,
    })
  }

  async register(data: RegisterData) {
    return this.request({
      method: 'POST',
      url: API_ENDPOINTS.AUTH.REGISTER,
      data,
    })
  }

  async logout() {
    return this.request({
      method: 'POST',
      url: API_ENDPOINTS.AUTH.LOGOUT,
    })
  }

  async refreshToken() {
    return this.request({
      method: 'POST',
      url: API_ENDPOINTS.AUTH.TOKEN_REFRESH,
    })
  }

  async getProfile(): Promise<UserProfile> {
    return this.request({
      method: 'GET',
      url: API_ENDPOINTS.AUTH.PROFILE,
    })
  }

  async updateProfile(data: Partial<UserProfile>): Promise<UserProfile> {
    return this.request({
      method: 'PUT',
      url: API_ENDPOINTS.AUTH.PROFILE,
      data,
    })
  }

  async changePassword(data: { current_password: string; new_password: string; new_password_confirm: string }) {
    return this.request({
      method: 'POST',
      url: API_ENDPOINTS.AUTH.PASSWORD_CHANGE,
      data,
    })
  }

  async exportUserData() {
    return this.request({
      method: 'GET',
      url: API_ENDPOINTS.AUTH.USER_DATA_EXPORT,
    })
  }

  async deleteAccount() {
    return this.request({
      method: 'DELETE',
      url: API_ENDPOINTS.AUTH.DELETE_ACCOUNT,
    })
  }

  // Contract Methods
  async getContracts(filters?: ContractFilters): Promise<ApiResponse<Contract>> {
    const params = new URLSearchParams()
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.append(key, String(value))
        }
      })
    }

    return this.request({
      method: 'GET',
      url: `${API_ENDPOINTS.NEXTCRM.CONTRACTS}?${params.toString()}`,
    })
  }

  async getContract(id: string): Promise<Contract> {
    return this.request({
      method: 'GET',
      url: `${API_ENDPOINTS.NEXTCRM.CONTRACTS}${id}/`,
    })
  }

  async createContract(data: ContractFormData): Promise<Contract> {
    return this.request({
      method: 'POST',
      url: API_ENDPOINTS.NEXTCRM.CONTRACTS,
      data,
    })
  }

  async updateContract(id: string, data: Partial<ContractFormData>): Promise<Contract> {
    return this.request({
      method: 'PUT',
      url: `${API_ENDPOINTS.NEXTCRM.CONTRACTS}${id}/`,
      data,
    })
  }

  async deleteContract(id: string) {
    return this.request({
      method: 'DELETE',
      url: `${API_ENDPOINTS.NEXTCRM.CONTRACTS}${id}/`,
    })
  }

  async approveContract(id: string) {
    return this.request({
      method: 'POST',
      url: `${API_ENDPOINTS.NEXTCRM.CONTRACTS}${id}/approve/`,
    })
  }

  async cancelContract(id: string, reason?: string) {
    return this.request({
      method: 'POST',
      url: `${API_ENDPOINTS.NEXTCRM.CONTRACTS}${id}/cancel/`,
      data: { reason },
    })
  }

  // Counterparty Methods
  async getCounterparties(params?: Record<string, any>): Promise<ApiResponse<Counterparty>> {
    return this.request({
      method: 'GET',
      url: API_ENDPOINTS.NEXTCRM.COUNTERPARTIES,
      params,
    })
  }

  async getCounterparty(id: number): Promise<Counterparty> {
    return this.request({
      method: 'GET',
      url: `${API_ENDPOINTS.NEXTCRM.COUNTERPARTIES}${id}/`,
    })
  }

  async createCounterparty(data: Partial<Counterparty>): Promise<Counterparty> {
    return this.request({
      method: 'POST',
      url: API_ENDPOINTS.NEXTCRM.COUNTERPARTIES,
      data,
    })
  }

  async updateCounterparty(id: number, data: Partial<Counterparty>): Promise<Counterparty> {
    return this.request({
      method: 'PUT',
      url: `${API_ENDPOINTS.NEXTCRM.COUNTERPARTIES}${id}/`,
      data,
    })
  }

  // Commodity Methods
  async getCommodities(params?: Record<string, any>): Promise<ApiResponse<Commodity>> {
    return this.request({
      method: 'GET',
      url: API_ENDPOINTS.NEXTCRM.COMMODITIES,
      params,
    })
  }

  async getCommodity(id: number): Promise<Commodity> {
    return this.request({
      method: 'GET',
      url: `${API_ENDPOINTS.NEXTCRM.COMMODITIES}${id}/`,
    })
  }

  // Trader Methods
  async getTraders(params?: Record<string, any>): Promise<ApiResponse<Trader>> {
    return this.request({
      method: 'GET',
      url: API_ENDPOINTS.NEXTCRM.TRADERS,
      params,
    })
  }

  async getTrader(id: number): Promise<Trader> {
    return this.request({
      method: 'GET',
      url: `${API_ENDPOINTS.NEXTCRM.TRADERS}${id}/`,
    })
  }

  // Currency Methods
  async getCurrencies(): Promise<ApiResponse<Currency>> {
    return this.request({
      method: 'GET',
      url: API_ENDPOINTS.NEXTCRM.CURRENCIES,
    })
  }

  // Reference Data Methods
  async getCostCenters() {
    return this.request({
      method: 'GET',
      url: API_ENDPOINTS.NEXTCRM.COST_CENTERS,
    })
  }

  async getSociedades() {
    return this.request({
      method: 'GET',
      url: API_ENDPOINTS.NEXTCRM.SOCIEDADES,
    })
  }

  async getCommodityGroups() {
    return this.request({
      method: 'GET',
      url: API_ENDPOINTS.NEXTCRM.COMMODITY_GROUPS,
    })
  }

  async getCommodityTypes() {
    return this.request({
      method: 'GET',
      url: API_ENDPOINTS.NEXTCRM.COMMODITY_TYPES,
    })
  }

  // Dashboard Methods
  async getDashboardStats(): Promise<DashboardStats> {
    return this.request({
      method: 'GET',
      url: API_ENDPOINTS.NEXTCRM.DASHBOARD_STATS,
    })
  }

  // Search Methods
  async globalSearch(query: string): Promise<GlobalSearchResults> {
    return this.request({
      method: 'GET',
      url: `${API_ENDPOINTS.NEXTCRM.SEARCH}?q=${encodeURIComponent(query)}`,
    })
  }
}

// Create and export singleton instance
export const apiClient = new ApiClient()
export default apiClient