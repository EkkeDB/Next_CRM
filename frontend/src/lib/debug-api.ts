import axios from 'axios'
import { API_URL } from './constants'

interface CORSDebugInfo {
  timestamp: string
  url: string
  method: string
  origin?: string
  status: number
  headers: Record<string, string>
  error?: string
  success: boolean
}

class CORSDebugger {
  private logs: CORSDebugInfo[] = []
  private maxLogs = 50

  private log(info: CORSDebugInfo) {
    this.logs.unshift(info)
    if (this.logs.length > this.maxLogs) {
      this.logs = this.logs.slice(0, this.maxLogs)
    }
    console.group(`🔍 CORS Debug: ${info.method} ${info.url}`)
    console.log('Status:', info.status)
    console.log('Success:', info.success)
    console.log('Origin:', info.origin || 'Not set')
    console.log('Headers:', info.headers)
    if (info.error) {
      console.error('Error:', info.error)
    }
    console.groupEnd()
  }

  async testBasicCORS(): Promise<CORSDebugInfo> {
    const url = `${API_URL}/api/auth/debug-cors`
    const info: CORSDebugInfo = {
      timestamp: new Date().toISOString(),
      url,
      method: 'GET',
      origin: window.location.origin,
      status: 0,
      headers: {},
      success: false
    }

    try {
      console.log('🧪 Testing basic CORS with:', url)
      
      const response = await fetch(url, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      info.status = response.status
      info.success = response.ok

      // Collect response headers
      response.headers.forEach((value, key) => {
        info.headers[key] = value
      })

      const data = await response.json()
      console.log('✅ CORS test response:', data)

    } catch (error: any) {
      info.error = error.message
      console.error('❌ CORS test failed:', error)
    }

    this.log(info)
    return info
  }

  async testAdvancedCORS(): Promise<CORSDebugInfo> {
    const url = `${API_URL}/api/auth/test-cors`
    const info: CORSDebugInfo = {
      timestamp: new Date().toISOString(),
      url,
      method: 'GET',
      origin: window.location.origin,
      status: 0,
      headers: {},
      success: false
    }

    try {
      console.log('🧪 Testing advanced CORS with:', url)
      
      const response = await fetch(url, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer test-token',
        },
      })

      info.status = response.status
      info.success = response.ok

      // Collect response headers
      response.headers.forEach((value, key) => {
        info.headers[key] = value
      })

      const data = await response.json()
      console.log('✅ Advanced CORS test response:', data)

    } catch (error: any) {
      info.error = error.message
      console.error('❌ Advanced CORS test failed:', error)
    }

    this.log(info)
    return info
  }

  async testProfileEndpoint(): Promise<CORSDebugInfo> {
    const url = `${API_URL}/api/auth/profile`
    const info: CORSDebugInfo = {
      timestamp: new Date().toISOString(),
      url,
      method: 'GET',
      origin: window.location.origin,
      status: 0,
      headers: {},
      success: false
    }

    try {
      console.log('🧪 Testing profile endpoint CORS with:', url)
      
      const response = await fetch(url, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      info.status = response.status
      info.success = response.ok || response.status === 401 // 401 is expected without auth

      // Collect response headers
      response.headers.forEach((value, key) => {
        info.headers[key] = value
      })

      const data = await response.json()
      console.log('📋 Profile endpoint response:', data)

    } catch (error: any) {
      info.error = error.message
      console.error('❌ Profile endpoint test failed:', error)
    }

    this.log(info)
    return info
  }

  async testAxiosRequest(): Promise<CORSDebugInfo> {
    const url = `${API_URL}/api/auth/debug-cors`
    const info: CORSDebugInfo = {
      timestamp: new Date().toISOString(),
      url,
      method: 'GET',
      origin: window.location.origin,
      status: 0,
      headers: {},
      success: false
    }

    try {
      console.log('🧪 Testing Axios CORS with:', url)
      
      const response = await axios.get(url, {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json',
        },
      })

      info.status = response.status
      info.success = response.status >= 200 && response.status < 300

      // Collect response headers
      Object.keys(response.headers).forEach(key => {
        info.headers[key] = response.headers[key]
      })

      console.log('✅ Axios CORS test response:', response.data)

    } catch (error: any) {
      if (error.response) {
        info.status = error.response.status
        Object.keys(error.response.headers || {}).forEach(key => {
          info.headers[key] = error.response.headers[key]
        })
      }
      info.error = error.message
      console.error('❌ Axios CORS test failed:', error)
    }

    this.log(info)
    return info
  }

  async runAllTests(): Promise<CORSDebugInfo[]> {
    console.log('🚀 Running comprehensive CORS debugging tests...')
    
    const results = await Promise.allSettled([
      this.testBasicCORS(),
      this.testAdvancedCORS(),
      this.testProfileEndpoint(),
      this.testAxiosRequest(),
    ])

    const testResults = results.map(result => 
      result.status === 'fulfilled' ? result.value : {
        timestamp: new Date().toISOString(),
        url: 'unknown',
        method: 'unknown',
        status: 0,
        headers: {},
        error: result.reason?.message || 'Test failed',
        success: false
      }
    )

    console.log('📊 All tests completed:', testResults)
    return testResults
  }

  getLogs(): CORSDebugInfo[] {
    return [...this.logs]
  }

  clearLogs(): void {
    this.logs = []
    console.log('🧹 CORS debug logs cleared')
  }

  printNetworkAnalysis(): void {
    console.group('🌐 Network Analysis')
    console.log('Current Origin:', window.location.origin)
    console.log('API URL:', API_URL)
    console.log('Protocol:', window.location.protocol)
    console.log('Hostname:', window.location.hostname)
    console.log('Port:', window.location.port || '(default)')
    console.log('User Agent:', navigator.userAgent)
    
    // Check if we're in a secure context
    console.log('Secure Context:', window.isSecureContext)
    
    // Check if service worker is registered
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.getRegistrations().then(registrations => {
        console.log('Service Workers:', registrations.length > 0 ? registrations : 'None')
      })
    }
    
    console.groupEnd()
  }
}

// Create singleton instance
export const corsDebugger = new CORSDebugger()

// Add to window for console access
if (typeof window !== 'undefined') {
  (window as any).corsDebugger = corsDebugger
}

export default corsDebugger