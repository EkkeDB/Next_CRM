'use client'

import { BarChart3, TrendingUp } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { formatCurrency, formatNumber } from '@/lib/utils'
import type { TopCommodity } from '@/types'

interface TopCommoditiesProps {
  data: TopCommodity[]
  isLoading?: boolean
}

export function TopCommodities({ data, isLoading }: TopCommoditiesProps) {
  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Top Commodities
          </CardTitle>
          <CardDescription>Highest value commodities by contract volume</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="h-12 bg-muted rounded-lg animate-pulse" />
            ))}
          </div>
        </CardContent>
      </Card>
    )
  }

  if (!data || data.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Top Commodities
          </CardTitle>
          <CardDescription>Highest value commodities by contract volume</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-muted-foreground">
            <BarChart3 className="h-12 w-12 mx-auto mb-2 opacity-50" />
            <p>No commodity data available</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  const maxValue = Math.max(...data.map(item => item.total_value))

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BarChart3 className="h-5 w-5" />
          Top Commodities
        </CardTitle>
        <CardDescription>
          Top {data.length} commodities by contract value
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {data.map((commodity, index) => {
            const percentage = (commodity.total_value / maxValue) * 100

            return (
              <div key={`${commodity.commodity_name}-${index}`} className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-sm">
                      #{index + 1}
                    </span>
                    <span className="font-medium">
                      {commodity.commodity_name}
                    </span>
                  </div>
                  <div className="text-right">
                    <div className="font-medium">
                      {formatCurrency(commodity.total_value)}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {formatNumber(commodity.contracts_count)} contract{commodity.contracts_count !== 1 ? 's' : ''}
                    </div>
                  </div>
                </div>
                <div className="w-full bg-muted rounded-full h-2">
                  <div
                    className="bg-primary h-2 rounded-full transition-all duration-300"
                    style={{ width: `${percentage}%` }}
                  />
                </div>
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}