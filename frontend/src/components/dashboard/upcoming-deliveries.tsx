'use client'

import { CalendarDays, Package, AlertCircle } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { formatDate, formatCurrency, cn } from '@/lib/utils'
import type { UpcomingDelivery } from '@/types'

interface UpcomingDeliveriesProps {
  data: UpcomingDelivery[]
  isLoading?: boolean
}

export function UpcomingDeliveries({ data, isLoading }: UpcomingDeliveriesProps) {
  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <CalendarDays className="h-5 w-5" />
            Upcoming Deliveries
          </CardTitle>
          <CardDescription>Contracts due for delivery in the next 30 days</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="h-16 bg-muted rounded-lg animate-pulse" />
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
            <CalendarDays className="h-5 w-5" />
            Upcoming Deliveries
          </CardTitle>
          <CardDescription>Contracts due for delivery in the next 30 days</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-muted-foreground">
            <Package className="h-12 w-12 mx-auto mb-2 opacity-50" />
            <p>No upcoming deliveries</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  const getUrgencyColor = (daysRemaining: number) => {
    if (daysRemaining <= 3) return 'text-red-600 bg-red-50 border-red-200'
    if (daysRemaining <= 7) return 'text-orange-600 bg-orange-50 border-orange-200'
    return 'text-blue-600 bg-blue-50 border-blue-200'
  }

  const getUrgencyIcon = (daysRemaining: number) => {
    if (daysRemaining <= 3) return <AlertCircle className="h-4 w-4" />
    return <CalendarDays className="h-4 w-4" />
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <CalendarDays className="h-5 w-5" />
          Upcoming Deliveries
        </CardTitle>
        <CardDescription>
          {data.length} contract{data.length !== 1 ? 's' : ''} due for delivery in the next 30 days
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {data.map((delivery, index) => (
            <div
              key={`${delivery.contract_number}-${index}`}
              className={cn(
                'flex items-center justify-between p-4 border rounded-lg',
                getUrgencyColor(delivery.days_remaining)
              )}
            >
              <div className="flex items-center gap-3">
                {getUrgencyIcon(delivery.days_remaining)}
                <div>
                  <div className="font-medium">
                    {delivery.contract_number}
                  </div>
                  <div className="text-sm opacity-80">
                    {delivery.counterparty_name} • {delivery.commodity_name}
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="font-medium">
                  {formatDate(delivery.delivery_date)}
                </div>
                <div className="text-sm opacity-80">
                  {delivery.days_remaining === 0 
                    ? 'Due today'
                    : delivery.days_remaining === 1
                    ? '1 day remaining'
                    : `${delivery.days_remaining} days remaining`
                  }
                </div>
                <div className="text-xs opacity-70">
                  {formatCurrency(delivery.total_value)}
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}