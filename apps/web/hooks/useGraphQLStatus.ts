import { useState, useEffect, useCallback } from 'react'

export interface HealthData {
  status: string
  timestamp: string
  api: {
    status: string
  }
  database: {
    status: string
    connection: boolean
    details: string | null
  }
}

export interface GraphQLStatus {
  isConnected: boolean
  isLoading: boolean
  error: string | null
  lastChecked: Date | null
  apiUrl: string
  healthData?: HealthData
}

export function useGraphQLStatus() {
  const [status, setStatus] = useState<GraphQLStatus>({
    isConnected: false,
    isLoading: true,
    error: null,
    lastChecked: null,
    apiUrl: '/api/graphql'
  })

  const checkStatus = useCallback(async () => {
    setStatus(prev => ({ ...prev, isLoading: true, error: null }))

    try {
      // Comprehensive health query
      const query = {
        query: `
          query {
            health {
              status
              timestamp
              api {
                status
              }
              database {
                status
                connection
                details
              }
            }
          }
        `
      }

      const response = await fetch('/api/graphql', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(query)
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const result = await response.json()

      if (result.errors) {
        throw new Error(result.errors[0]?.message || 'GraphQL query failed')
      }

      const healthData = result.data?.health
      const overallHealthy = healthData?.status === 'ok'
      
      setStatus({
        isConnected: overallHealthy,
        isLoading: false,
        error: null,
        lastChecked: new Date(),
        apiUrl: '/api/graphql',
        healthData: healthData
      })
    } catch (error) {
      setStatus(prev => ({
        ...prev,
        isConnected: false,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        lastChecked: new Date()
      }))
    }
  }, [])

  // Check status on mount and set up periodic checking
  useEffect(() => {
    checkStatus()

    const interval = setInterval(checkStatus, 30000) // Check every 30 seconds

    return () => clearInterval(interval)
  }, [checkStatus])

  return {
    ...status,
    refetch: checkStatus
  }
}
