export const APP_NAME = process.env.NEXT_PUBLIC_APP_NAME || 'NextCRM'
export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// API Endpoints
export const API_ENDPOINTS = {
  // Authentication
  AUTH: {
    LOGIN: '/api/auth/login/',
    LOGOUT: '/api/auth/logout/',
    REGISTER: '/api/auth/register/',
    PROFILE: '/api/auth/profile/',
    TOKEN_REFRESH: '/api/auth/token/refresh/',
    PASSWORD_CHANGE: '/api/auth/password/change/',
    GDPR_CONSENT: '/api/auth/gdpr/consent/',
    USER_DATA_EXPORT: '/api/auth/gdpr/export/',
    DELETE_ACCOUNT: '/api/auth/account/delete/',
  },
  
  // Core Business
  NEXTCRM: {
    CONTRACTS: '/api/nextcrm/contracts/',
    COUNTERPARTIES: '/api/nextcrm/counterparties/',
    COMMODITIES: '/api/nextcrm/commodities/',
    TRADERS: '/api/nextcrm/traders/',
    CURRENCIES: '/api/nextcrm/currencies/',
    COST_CENTERS: '/api/nextcrm/cost-centers/',
    SOCIEDADES: '/api/nextcrm/sociedades/',
    COMMODITY_GROUPS: '/api/nextcrm/commodity-groups/',
    COMMODITY_TYPES: '/api/nextcrm/commodity-types/',
    EXCHANGE_RATES: '/api/nextcrm/exchange-rates/',
    CONTRACT_AMENDMENTS: '/api/nextcrm/contract-amendments/',
    SEARCH: '/api/nextcrm/search/',
    DASHBOARD_STATS: '/api/nextcrm/contracts/dashboard_stats/',
  },
} as const

// Contract Status Options
export const CONTRACT_STATUS_OPTIONS = [
  { value: 'draft', label: 'Draft', color: 'bg-gray-100 text-gray-800' },
  { value: 'pending_approval', label: 'Pending Approval', color: 'bg-yellow-100 text-yellow-800' },
  { value: 'approved', label: 'Approved', color: 'bg-blue-100 text-blue-800' },
  { value: 'executed', label: 'Executed', color: 'bg-green-100 text-green-800' },
  { value: 'partially_executed', label: 'Partially Executed', color: 'bg-orange-100 text-orange-800' },
  { value: 'completed', label: 'Completed', color: 'bg-green-100 text-green-800' },
  { value: 'cancelled', label: 'Cancelled', color: 'bg-red-100 text-red-800' },
  { value: 'expired', label: 'Expired', color: 'bg-gray-100 text-gray-800' },
] as const

// Counterparty Type Options
export const COUNTERPARTY_TYPE_OPTIONS = [
  { value: 'supplier', label: 'Supplier' },
  { value: 'customer', label: 'Customer' },
  { value: 'both', label: 'Both' },
] as const

// Delivery Terms (Incoterms)
export const DELIVERY_TERMS_OPTIONS = [
  { value: 'FOB', label: 'FOB - Free on Board' },
  { value: 'CIF', label: 'CIF - Cost, Insurance, and Freight' },
  { value: 'CFR', label: 'CFR - Cost and Freight' },
  { value: 'EXW', label: 'EXW - Ex Works' },
  { value: 'FCA', label: 'FCA - Free Carrier' },
  { value: 'CPT', label: 'CPT - Carriage Paid To' },
  { value: 'CIP', label: 'CIP - Carriage and Insurance Paid To' },
  { value: 'DAP', label: 'DAP - Delivered at Place' },
  { value: 'DPU', label: 'DPU - Delivered at Place Unloaded' },
  { value: 'DDP', label: 'DDP - Delivered Duty Paid' },
] as const

// Amendment Types
export const AMENDMENT_TYPE_OPTIONS = [
  { value: 'quantity', label: 'Quantity Change' },
  { value: 'price', label: 'Price Change' },
  { value: 'delivery_date', label: 'Delivery Date Change' },
  { value: 'quality', label: 'Quality Specification Change' },
  { value: 'other', label: 'Other' },
] as const

// Credit Rating Options
export const CREDIT_RATING_OPTIONS = [
  { value: 'AAA', label: 'AAA' },
  { value: 'AA', label: 'AA' },
  { value: 'A', label: 'A' },
  { value: 'BBB', label: 'BBB' },
  { value: 'BB', label: 'BB' },
  { value: 'B', label: 'B' },
  { value: 'CCC', label: 'CCC' },
  { value: 'CC', label: 'CC' },
  { value: 'C', label: 'C' },
  { value: 'D', label: 'D' },
] as const

// Common Units of Measure
export const UNIT_OF_MEASURE_OPTIONS = [
  { value: 'MT', label: 'Metric Tons (MT)' },
  { value: 'KG', label: 'Kilograms (KG)' },
  { value: 'LBS', label: 'Pounds (LBS)' },
  { value: 'BBL', label: 'Barrels (BBL)' },
  { value: 'GAL', label: 'Gallons (GAL)' },
  { value: 'L', label: 'Liters (L)' },
  { value: 'M3', label: 'Cubic Meters (M³)' },
  { value: 'FT3', label: 'Cubic Feet (FT³)' },
] as const

// Date Formats
export const DATE_FORMATS = {
  DISPLAY: 'MMM dd, yyyy',
  INPUT: 'yyyy-MM-dd',
  FULL: 'MMMM dd, yyyy',
  SHORT: 'MM/dd/yyyy',
  ISO: "yyyy-MM-dd'T'HH:mm:ss.SSSxxx",
} as const

// Pagination
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
} as const

// Chart Colors
export const CHART_COLORS = {
  PRIMARY: '#3b82f6',
  SECONDARY: '#64748b',
  SUCCESS: '#10b981',
  WARNING: '#f59e0b',
  DANGER: '#ef4444',
  INFO: '#06b6d4',
  LIGHT: '#e2e8f0',
  DARK: '#1e293b',
} as const

// Toast Messages
export const TOAST_MESSAGES = {
  SUCCESS: {
    LOGIN: 'Successfully logged in!',
    LOGOUT: 'Successfully logged out!',
    REGISTER: 'Account created successfully!',
    CONTRACT_CREATED: 'Contract created successfully!',
    CONTRACT_UPDATED: 'Contract updated successfully!',
    CONTRACT_APPROVED: 'Contract approved successfully!',
    CONTRACT_CANCELLED: 'Contract cancelled successfully!',
    COUNTERPARTY_CREATED: 'Counterparty created successfully!',
    COUNTERPARTY_UPDATED: 'Counterparty updated successfully!',
    PROFILE_UPDATED: 'Profile updated successfully!',
    PASSWORD_CHANGED: 'Password changed successfully!',
  },
  ERROR: {
    GENERIC: 'Something went wrong. Please try again.',
    LOGIN_FAILED: 'Invalid credentials. Please try again.',
    NETWORK_ERROR: 'Network error. Please check your connection.',
    UNAUTHORIZED: 'You are not authorized to perform this action.',
    VALIDATION_ERROR: 'Please check your input and try again.',
    CONTRACT_NOT_FOUND: 'Contract not found.',
    COUNTERPARTY_NOT_FOUND: 'Counterparty not found.',
  },
} as const

// Local Storage Keys
export const STORAGE_KEYS = {
  THEME: 'nextcrm-theme',
  SIDEBAR_COLLAPSED: 'nextcrm-sidebar-collapsed',
  TABLE_FILTERS: 'nextcrm-table-filters',
  USER_PREFERENCES: 'nextcrm-user-preferences',
} as const

// Query Keys for React Query
export const QUERY_KEYS = {
  USER: 'user',
  PROFILE: 'profile',
  CONTRACTS: 'contracts',
  CONTRACT: 'contract',
  COUNTERPARTIES: 'counterparties',
  COUNTERPARTY: 'counterparty',
  COMMODITIES: 'commodities',
  COMMODITY: 'commodity',
  TRADERS: 'traders',
  TRADER: 'trader',
  CURRENCIES: 'currencies',
  DASHBOARD_STATS: 'dashboard-stats',
  SEARCH: 'search',
  COST_CENTERS: 'cost-centers',
  SOCIEDADES: 'sociedades',
  COMMODITY_GROUPS: 'commodity-groups',
  COMMODITY_TYPES: 'commodity-types',
} as const