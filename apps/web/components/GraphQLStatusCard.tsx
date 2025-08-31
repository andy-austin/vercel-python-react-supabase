'use client'

import { useGraphQLStatus } from '@/hooks/useGraphQLStatus'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

const StatusIndicator = ({ status, isLoading }: { status?: string; isLoading: boolean }) => {
  if (isLoading) {
    return <Badge variant="secondary" className="animate-pulse">Checking...</Badge>
  }

  const getStatusVariant = (status?: string) => {
    switch (status) {
      case 'ok':
        return { variant: 'default' as const, label: 'Healthy' }
      case 'degraded':
        return { variant: 'secondary' as const, label: 'Degraded' }
      case 'error':
        return { variant: 'destructive' as const, label: 'Error' }
      default:
        return { variant: 'outline' as const, label: 'Unknown' }
    }
  }

  const { variant, label } = getStatusVariant(status)
  return <Badge variant={variant}>{label}</Badge>
}

export default function GraphQLStatusCard() {
  const { isConnected, isLoading, error, lastChecked, apiUrl, healthData, refetch } = useGraphQLStatus()

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>GraphQL API Status</CardTitle>
            <CardDescription>Monitor the health of your API services</CardDescription>
          </div>
          <Button
            onClick={refetch}
            disabled={isLoading}
            variant="outline"
            size="sm"
          >
            {isLoading ? 'Checking...' : 'Refresh'}
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <StatusIndicator status={healthData?.status} isLoading={isLoading} />
        </div>

        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">Endpoint:</span>
          <code className="text-sm bg-muted px-2 py-1 rounded font-mono">{apiUrl}</code>
        </div>

        {lastChecked && (
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">Last checked:</span>
            <span className="text-sm">{lastChecked.toLocaleTimeString()}</span>
          </div>
        )}

        {healthData && (
          <div className="space-y-4">
            <div className="border-t pt-4">
              <h3 className="text-sm font-medium mb-3">Service Status</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <Card className="p-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">API</span>
                    <Badge variant={healthData.api.status === 'ok' ? 'default' : 'destructive'}>
                      {healthData.api.status}
                    </Badge>
                  </div>
                </Card>

                <Card className="p-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Database</span>
                    <Badge 
                      variant={
                        healthData.database.status === 'ok' ? 'default' : 
                        healthData.database.status === 'error' ? 'destructive' : 'secondary'
                      }
                    >
                      {healthData.database.connection ? 'Connected' : 'Disconnected'}
                    </Badge>
                  </div>
                </Card>
              </div>

              {healthData.database.details && (
                <Card className="mt-3 p-3 bg-muted/50">
                  <div className="text-sm">
                    <strong>DB Details:</strong> {healthData.database.details}
                  </div>
                </Card>
              )}
            </div>

            <div className="text-xs text-muted-foreground">
              Server time: {new Date(healthData.timestamp).toLocaleString()}
            </div>
          </div>
        )}

        {error && (
          <Card className="border-destructive/50 bg-destructive/10">
            <CardContent className="pt-6">
              <div className="text-destructive text-sm">
                <strong>Error:</strong> {error}
              </div>
            </CardContent>
          </Card>
        )}

        {healthData?.status === 'ok' && (
          <Card className="border-green-500/50 bg-green-50">
            <CardContent className="pt-6">
              <div className="text-green-700 text-sm">
                ✓ All systems operational
              </div>
            </CardContent>
          </Card>
        )}

        {healthData?.status === 'degraded' && (
          <Card className="border-yellow-500/50 bg-yellow-50">
            <CardContent className="pt-6">
              <div className="text-yellow-700 text-sm">
                ⚠ Some services may be experiencing issues
              </div>
            </CardContent>
          </Card>
        )}
      </CardContent>
    </Card>
  )
}
