'use client'

import { useGraphQLStatus } from '@/hooks/useGraphQLStatus'

const StatusIndicator = ({ isConnected, isLoading }: { isConnected: boolean; isLoading: boolean }) => {
  if (isLoading) {
    return (
      <div className="flex items-center">
        <div className="w-3 h-3 bg-yellow-400 rounded-full animate-pulse mr-2"></div>
        <span className="text-yellow-600">Checking...</span>
      </div>
    )
  }

  return (
    <div className="flex items-center">
      <div className={`w-3 h-3 rounded-full mr-2 ${
        isConnected ? 'bg-green-400' : 'bg-red-400'
      }`}></div>
      <span className={isConnected ? 'text-green-600' : 'text-red-600'}>
        {isConnected ? 'Connected' : 'Disconnected'}
      </span>
    </div>
  )
}

export default function GraphQLStatusCard() {
  const { isConnected, isLoading, error, lastChecked, apiUrl, helloMessage, refetch } = useGraphQLStatus()

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

      <div className="space-y-3">
        <div>
          <StatusIndicator isConnected={isConnected} isLoading={isLoading} />
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

        {helloMessage && (
          <div>
            <span className="text-gray-600 text-sm">Response: </span>
            <span className="text-sm text-green-600">&ldquo;{helloMessage}&rdquo;</span>
          </div>
        )}

        {error && (
          <div className="mt-3 p-3 bg-red-50 border-l-4 border-red-400">
            <div className="text-red-700 text-sm">
              <strong>Error:</strong> {error}
            </div>
          </div>
        )}

        {isConnected && (
          <div className="mt-3 p-3 bg-green-50 border-l-4 border-green-400">
            <div className="text-green-700 text-sm">
              ✓ GraphQL API is running and accessible
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
