// API Response Types
export interface ApiResponse<T> {
  results: T[]
  count: number
  next: string | null
  previous: string | null
}

// User and Authentication Types
export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  date_joined: string
  last_login: string | null
}

export interface UserProfile {
  username: string
  email: string
  first_name: string
  last_name: string
  phone: string
  company: string
  position: string
  timezone: string
  date_joined: string
  last_login: string | null
  gdpr_consent: boolean
  gdpr_consent_date: string | null
  is_mfa_enabled: boolean
}

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  first_name: string
  last_name: string
  password: string
  password_confirm: string
  phone?: string
  company?: string
  position?: string
  gdpr_consent: boolean
}

// Business Entity Types
export interface CostCenter {
  id: number
  cost_center_name: string
  description: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Sociedad {
  id: number
  sociedad_name: string
  tax_id: string
  address: string
  city: string
  country: string
  phone: string
  email: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Trader {
  id: number
  trader_name: string
  email: string
  phone: string
  employee_id: string
  department: string
  hire_date: string | null
  is_active: boolean
  user: number | null
  created_at: string
  updated_at: string
}

export interface CommodityGroup {
  id: number
  commodity_group_name: string
  description: string
  sort_order: number
  is_active: boolean
  commodities_count?: number
  created_at: string
  updated_at: string
}

export interface CommodityType {
  id: number
  commodity_type_name: string
  description: string
  sort_order: number
  is_active: boolean
  commodities_count?: number
  created_at: string
  updated_at: string
}

export interface Commodity {
  id: number
  commodity_name_short: string
  commodity_name_full: string
  commodity_group: number
  commodity_group_name?: string
  commodity_type: number
  commodity_type_name?: string
  commodity_code: string
  default_unit: string
  quality_specifications: string
  is_active: boolean
  active_contracts_count?: number
  created_at: string
  updated_at: string
}

export interface Counterparty {
  id: number
  counterparty_name: string
  counterparty_code: string
  tax_id: string
  address: string
  city: string
  state_province: string
  postal_code: string
  country: string
  phone: string
  email: string
  website: string
  counterparty_type: 'supplier' | 'customer' | 'both'
  credit_rating: string
  credit_limit: number | null
  payment_terms: string
  primary_contact_name: string
  primary_contact_email: string
  primary_contact_phone: string
  is_active: boolean
  is_blacklisted: boolean
  blacklist_reason: string
  notes: string
  contracts_count?: number
  total_contract_value?: number
  last_contract_date?: string
  created_at: string
  updated_at: string
}

export interface Currency {
  id: number
  currency_code: string
  currency_name: string
  currency_symbol: string
  is_base_currency: boolean
  is_active: boolean
  decimal_places: number
  created_at: string
  updated_at: string
}

export interface Contract {
  id: string
  contract_number: string
  trader: number
  trader_name?: string
  counterparty: number
  counterparty_name?: string
  commodity: number
  commodity_name?: string
  commodity_group_name?: string
  cost_center: number | null
  cost_center_name?: string
  sociedad: number | null
  sociedad_name?: string
  
  // Commercial terms
  quantity: number
  unit_of_measure: string
  price: number
  trade_currency: number
  currency_code?: string
  price_basis: string
  premium_discount: number
  total_value: number
  
  // Delivery terms
  delivery_terms: string
  delivery_location: string
  loading_port: string
  discharge_port: string
  
  // Dates
  contract_date: string
  delivery_period_start: string
  delivery_period_end: string
  shipment_period_start: string | null
  shipment_period_end: string | null
  
  // Status and workflow
  status: 'draft' | 'pending_approval' | 'approved' | 'executed' | 'partially_executed' | 'completed' | 'cancelled' | 'expired'
  approval_date: string | null
  approved_by: number | null
  approved_by_username?: string
  
  // Quality and specifications
  quality_specifications: string
  inspection_terms: string
  
  // Risk management
  hedge_required: boolean
  hedge_percentage: number
  
  // Additional terms
  payment_terms: string
  force_majeure_clause: string
  special_conditions: string
  notes: string
  
  // Internal tracking
  internal_reference: string
  profit_center: string
  
  // Computed fields
  days_to_delivery: number | null
  is_overdue: boolean
  completion_percentage: number
  
  // Metadata
  created_at: string
  updated_at: string
  created_by: number | null
  created_by_username?: string
  updated_by: number | null
  updated_by_username?: string
  
  // Related data
  amendments?: ContractAmendment[]
}

export interface ContractAmendment {
  id: number
  contract: string
  amendment_number: string
  amendment_type: 'quantity' | 'price' | 'delivery_date' | 'quality' | 'other'
  description: string
  old_values: Record<string, any>
  new_values: Record<string, any>
  requested_by: number
  requested_by_username?: string
  approved_by: number | null
  approved_by_username?: string
  approval_date: string | null
  created_at: string
}

// Dashboard and Statistics Types
export interface DashboardStats {
  total_contracts: number
  active_contracts: number
  completed_contracts: number
  total_value: number
  total_counterparties: number
  overdue_contracts: number
  monthly_contracts: MonthlyData[]
  monthly_revenue: MonthlyData[]
  status_distribution: Record<string, StatusDistribution>
  top_commodities: TopCommodity[]
  top_counterparties: TopCounterparty[]
  upcoming_deliveries: UpcomingDelivery[]
}

export interface MonthlyData {
  month: string
  contracts_count?: number
  total_value?: number
}

export interface StatusDistribution {
  count: number
  percentage: number
}

export interface TopCommodity {
  commodity_name: string
  contracts_count: number
  total_value: number
}

export interface TopCounterparty {
  counterparty_name: string
  contracts_count: number
  total_value: number
}

export interface UpcomingDelivery {
  contract_number: string
  counterparty_name: string
  commodity_name: string
  delivery_date: string
  days_remaining: number
  total_value: number
}

// Search Types
export interface GlobalSearchResults {
  contracts: ContractSearchResult[]
  counterparties: CounterpartySearchResult[]
  commodities: CommoditySearchResult[]
  traders: TraderSearchResult[]
}

export interface ContractSearchResult {
  id: string
  contract_number: string
  counterparty_name: string
  commodity_name: string
  total_value: number
  status: string
}

export interface CounterpartySearchResult {
  id: number
  counterparty_name: string
  counterparty_type: string
  city: string
  country: string
}

export interface CommoditySearchResult {
  id: number
  commodity_name_short: string
  commodity_name_full: string
  commodity_group: string
}

export interface TraderSearchResult {
  id: number
  trader_name: string
  email: string
  department: string
}

// Form Types
export interface ContractFormData {
  trader: number
  counterparty: number
  commodity: number
  cost_center?: number
  sociedad?: number
  quantity: number
  unit_of_measure: string
  price: number
  trade_currency: number
  price_basis?: string
  premium_discount?: number
  delivery_terms: string
  delivery_location?: string
  loading_port?: string
  discharge_port?: string
  contract_date: string
  delivery_period_start: string
  delivery_period_end: string
  shipment_period_start?: string
  shipment_period_end?: string
  quality_specifications?: string
  inspection_terms?: string
  hedge_required?: boolean
  hedge_percentage?: number
  payment_terms?: string
  force_majeure_clause?: string
  special_conditions?: string
  notes?: string
  internal_reference?: string
  profit_center?: string
}

// Filter and Pagination Types
export interface ContractFilters {
  status?: string
  trader?: number
  counterparty?: number
  commodity_group?: number
  contract_date_after?: string
  contract_date_before?: string
  search?: string
  ordering?: string
  page?: number
  page_size?: number
}

export interface PaginationParams {
  page?: number
  page_size?: number
}

// Error Types
export interface ApiError {
  message: string
  errors?: Record<string, string[]>
  detail?: string
}