'use client'

import { useGraphQLStatus } from '@/hooks/useGraphQLStatus'

const StatusIndicator = ({ status, isLoading }: { status?: string; isLoading: boolean }) => {
  if (isLoading) {
    return (
      <div className="flex items-center">
        <div className="w-3 h-3 bg-yellow-400 rounded-full animate-pulse mr-2"></div>
        <span className="text-yellow-600">Checking...</span>
      </div>
    )
  }

  const getStatusColor = (status?: string) => {
    switch (status) {
      case 'ok':
        return { bg: 'bg-green-400', text: 'text-green-600', label: 'Healthy' }
      case 'degraded':
        return { bg: 'bg-yellow-400', text: 'text-yellow-600', label: 'Degraded' }
      case 'error':
        return { bg: 'bg-red-400', text: 'text-red-600', label: 'Error' }
      default:
        return { bg: 'bg-gray-400', text: 'text-gray-600', label: 'Unknown' }
    }
  }

  const { bg, text, label } = getStatusColor(status)

  return (
    <div className="flex items-center">
      <div className={`w-3 h-3 rounded-full mr-2 ${bg}`}></div>
      <span className={text}>{label}</span>
    </div>
  )
}

export default function GraphQLStatusCard() {
  const { isConnected, isLoading, error, lastChecked, apiUrl, healthData, refetch } = useGraphQLStatus()

  return (
    <div className="border rounded-lg p-6 bg-white shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">GraphQL API Status</h2>
        <button
          onClick={refetch}
          className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          disabled={isLoading}
        >
          {isLoading ? 'Checking...' : 'Refresh'}
        </button>
      </div>

      <div className="space-y-4">
        <div>
          <StatusIndicator status={healthData?.status} isLoading={isLoading} />
        </div>

        <div>
          <span className="text-gray-600 text-sm">Endpoint: </span>
          <code className="text-sm bg-gray-100 px-2 py-1 rounded">{apiUrl}</code>
        </div>

        {lastChecked && (
          <div>
            <span className="text-gray-600 text-sm">Last checked: </span>
            <span className="text-sm">{lastChecked.toLocaleTimeString()}</span>
          </div>
        )}

        {healthData && (
          <div className="space-y-3">
            <div className="border-t pt-3">
              <h3 className="text-sm font-medium text-gray-700 mb-2">Service Status</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">API</span>
                    <div className={`w-2 h-2 rounded-full ${
                      healthData.api.status === 'ok' ? 'bg-green-400' : 'bg-red-400'
                    }`}></div>
                  </div>
                  <span className="text-xs text-gray-600">{healthData.api.status}</span>
                </div>

                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Database</span>
                    <div className={`w-2 h-2 rounded-full ${
                      healthData.database.status === 'ok' ? 'bg-green-400' : 
                      healthData.database.status === 'error' ? 'bg-red-400' : 'bg-yellow-400'
                    }`}></div>
                  </div>
                  <span className="text-xs text-gray-600">
                    {healthData.database.connection ? 'Connected' : 'Disconnected'}
                  </span>
                </div>
              </div>

              {healthData.database.details && (
                <div className="mt-3 p-2 bg-blue-50 rounded text-xs text-blue-700">
                  <strong>DB Details:</strong> {healthData.database.details}
                </div>
              )}
            </div>

            <div className="text-xs text-gray-500">
              Server time: {new Date(healthData.timestamp).toLocaleString()}
            </div>
          </div>
        )}

        {error && (
          <div className="mt-3 p-3 bg-red-50 border-l-4 border-red-400">
            <div className="text-red-700 text-sm">
              <strong>Error:</strong> {error}
            </div>
          </div>
        )}

        {healthData?.status === 'ok' && (
          <div className="mt-3 p-3 bg-green-50 border-l-4 border-green-400">
            <div className="text-green-700 text-sm">
              ✓ All systems operational
            </div>
          </div>
        )}

        {healthData?.status === 'degraded' && (
          <div className="mt-3 p-3 bg-yellow-50 border-l-4 border-yellow-400">
            <div className="text-yellow-700 text-sm">
              ⚠ Some services may be experiencing issues
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
