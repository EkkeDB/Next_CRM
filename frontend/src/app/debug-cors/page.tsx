'use client'

import { useState, useEffect } from 'react'
import { corsDebugger } from '@/lib/debug-api'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'

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

export default function CORSDebugPage() {
  const [logs, setLogs] = useState<CORSDebugInfo[]>([])
  const [loading, setLoading] = useState(false)
  const [networkInfo, setNetworkInfo] = useState<any>(null)

  useEffect(() => {
    // Gather network info
    setNetworkInfo({
      origin: window.location.origin,
      protocol: window.location.protocol,
      hostname: window.location.hostname,
      port: window.location.port || '(default)',
      userAgent: navigator.userAgent,
      secureContext: window.isSecureContext,
    })

    // Print network analysis to console
    corsDebugger.printNetworkAnalysis()
  }, [])

  const runTest = async (testName: string, testFn: () => Promise<CORSDebugInfo>) => {
    setLoading(true)
    try {
      await testFn()
      setLogs(corsDebugger.getLogs())
    } catch (error) {
      console.error(`Test ${testName} failed:`, error)
    } finally {
      setLoading(false)
    }
  }

  const runAllTests = async () => {
    setLoading(true)
    try {
      await corsDebugger.runAllTests()
      setLogs(corsDebugger.getLogs())
    } catch (error) {
      console.error('All tests failed:', error)
    } finally {
      setLoading(false)
    }
  }

  const clearLogs = () => {
    corsDebugger.clearLogs()
    setLogs([])
  }

  const getStatusColor = (status: number, success: boolean) => {
    if (!success) return 'text-red-600'
    if (status >= 200 && status < 300) return 'text-green-600'
    if (status >= 300 && status < 400) return 'text-yellow-600'
    if (status >= 400 && status < 500) return 'text-orange-600'
    return 'text-red-600'
  }

  return (
    <div className="container mx-auto p-6 max-w-6xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">CORS Debugging Dashboard</h1>
        <p className="text-gray-600">
          Comprehensive CORS debugging tools to identify cross-origin request issues.
        </p>
      </div>

      {/* Network Information */}
      <Card className="p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Network Information</h2>
        {networkInfo && (
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
            <div>
              <strong>Origin:</strong> {networkInfo.origin}
            </div>
            <div>
              <strong>Protocol:</strong> {networkInfo.protocol}
            </div>
            <div>
              <strong>Hostname:</strong> {networkInfo.hostname}
            </div>
            <div>
              <strong>Port:</strong> {networkInfo.port}
            </div>
            <div>
              <strong>Secure Context:</strong> {networkInfo.secureContext ? 'Yes' : 'No'}
            </div>
            <div className="col-span-2 md:col-span-3">
              <strong>User Agent:</strong> {networkInfo.userAgent}
            </div>
          </div>
        )}
      </Card>

      {/* Test Controls */}
      <Card className="p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">CORS Tests</h2>
        <div className="flex flex-wrap gap-3">
          <Button 
            onClick={() => runTest('Basic CORS', corsDebugger.testBasicCORS)}
            disabled={loading}
            variant="outline"
          >
            Test Basic CORS
          </Button>
          <Button 
            onClick={() => runTest('Advanced CORS', corsDebugger.testAdvancedCORS)}
            disabled={loading}
            variant="outline"
          >
            Test Advanced CORS
          </Button>
          <Button 
            onClick={() => runTest('Profile Endpoint', corsDebugger.testProfileEndpoint)}
            disabled={loading}
            variant="outline"
          >
            Test Profile Endpoint
          </Button>
          <Button 
            onClick={() => runTest('Axios Request', corsDebugger.testAxiosRequest)}
            disabled={loading}
            variant="outline"
          >
            Test Axios
          </Button>
          <Button 
            onClick={runAllTests}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700"
          >
            {loading ? 'Running Tests...' : 'Run All Tests'}
          </Button>
          <Button 
            onClick={clearLogs}
            variant="outline"
            className="text-red-600 border-red-300 hover:bg-red-50"
          >
            Clear Logs
          </Button>
        </div>
      </Card>

      {/* Debug Instructions */}
      <Card className="p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Debugging Instructions</h2>
        <div className="space-y-2 text-sm">
          <p><strong>1.</strong> Open your browser's Developer Tools (F12)</p>
          <p><strong>2.</strong> Go to the Network tab</p>
          <p><strong>3.</strong> Run the tests above</p>
          <p><strong>4.</strong> Look for failed requests (red status)</p>
          <p><strong>5.</strong> Check the Console tab for detailed CORS logs</p>
          <p><strong>6.</strong> Compare browser headers with server expectations</p>
        </div>
      </Card>

      {/* Test Results */}
      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Test Results ({logs.length})</h2>
        {logs.length === 0 ? (
          <p className="text-gray-500">No tests run yet. Click one of the test buttons above.</p>
        ) : (
          <div className="space-y-4">
            {logs.map((log, index) => (
              <div key={index} className="border rounded-lg p-4 bg-gray-50">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-3">
                    <span className="font-mono text-sm bg-gray-200 px-2 py-1 rounded">
                      {log.method}
                    </span>
                    <span className={`font-semibold ${getStatusColor(log.status, log.success)}`}>
                      {log.status}
                    </span>
                    <span className={`text-sm ${log.success ? 'text-green-600' : 'text-red-600'}`}>
                      {log.success ? '✅ Success' : '❌ Failed'}
                    </span>
                  </div>
                  <span className="text-xs text-gray-500">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                
                <div className="text-sm mb-2">
                  <strong>URL:</strong> <code className="bg-gray-100 px-1 rounded">{log.url}</code>
                </div>
                
                {log.origin && (
                  <div className="text-sm mb-2">
                    <strong>Origin:</strong> <code className="bg-gray-100 px-1 rounded">{log.origin}</code>
                  </div>
                )}
                
                {log.error && (
                  <div className="text-sm mb-2 text-red-600">
                    <strong>Error:</strong> {log.error}
                  </div>
                )}
                
                {Object.keys(log.headers).length > 0 && (
                  <details className="text-sm">
                    <summary className="cursor-pointer font-medium mb-1">
                      Response Headers ({Object.keys(log.headers).length})
                    </summary>
                    <div className="bg-gray-100 p-2 rounded font-mono text-xs">
                      {Object.entries(log.headers).map(([key, value]) => (
                        <div key={key} className="mb-1">
                          <span className="text-blue-600">{key}:</span> {value}
                        </div>
                      ))}
                    </div>
                  </details>
                )}
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* Console Instructions */}
      <Card className="p-6 mt-6">
        <h2 className="text-xl font-semibold mb-4">Console Debugging</h2>
        <div className="bg-gray-100 p-4 rounded font-mono text-sm">
          <p className="mb-2">You can also run tests from the browser console:</p>
          <div className="space-y-1 text-green-700">
            <p>corsDebugger.runAllTests()</p>
            <p>corsDebugger.testBasicCORS()</p>
            <p>corsDebugger.testProfileEndpoint()</p>
            <p>corsDebugger.getLogs()</p>
            <p>corsDebugger.printNetworkAnalysis()</p>
          </div>
        </div>
      </Card>
    </div>
  )
}