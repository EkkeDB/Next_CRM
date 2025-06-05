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
        if (error.response?.status === 401) {
          // Try to refresh token
          try {
            await this.refreshToken()
            // Retry the original request
            return this.instance(error.config)
          } catch (refreshError) {
            // Refresh failed, redirect to login
            if (typeof window !== 'undefined') {
              window.location.href = '/login'
            }
            return Promise.reject(refreshError)
          }
        }
        return Promise.reject(error)
      }
    )
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