'use client'

import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { getContractStatusLabel } from '@/lib/utils'
import type { StatusDistribution } from '@/types'

interface StatusDistributionProps {
  data: Record<string, StatusDistribution>
  isLoading?: boolean
}

const STATUS_COLORS = {
  draft: '#6b7280',
  pending_approval: '#f59e0b',
  approved: '#3b82f6',
  executed: '#10b981',
  partially_executed: '#f97316',
  completed: '#059669',
  cancelled: '#ef4444',
  expired: '#6b7280',
}

export function StatusDistributionChart({ data, isLoading }: StatusDistributionProps) {
  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Contract Status</CardTitle>
          <CardDescription>Distribution of contract statuses</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[350px] w-full bg-muted rounded-lg animate-pulse" />
        </CardContent>
      </Card>
    )
  }

  if (!data || Object.keys(data).length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Contract Status</CardTitle>
          <CardDescription>Distribution of contract statuses</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[350px] flex items-center justify-center text-muted-foreground">
            No status data available
          </div>
        </CardContent>
      </Card>
    )
  }

  // Transform data for pie chart
  const chartData = Object.entries(data)
    .filter(([_, value]) => value.count > 0)
    .map(([status, value]) => ({
      name: getContractStatusLabel(status),
      value: value.count,
      percentage: value.percentage,
      color: STATUS_COLORS[status as keyof typeof STATUS_COLORS] || '#6b7280',
    }))

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-background border border-border rounded-lg shadow-lg p-3">
          <p className="font-medium">{data.name}</p>
          <p style={{ color: data.color }}>
            Count: {data.value} ({data.percentage}%)
          </p>
        </div>
      )
    }
    return null
  }

  const renderCustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percentage }: any) => {
    if (percentage < 5) return null // Don't show label for small slices
    
    const RADIAN = Math.PI / 180
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5
    const x = cx + radius * Math.cos(-midAngle * RADIAN)
    const y = cy + radius * Math.sin(-midAngle * RADIAN)

    return (
      <text
        x={x}
        y={y}
        fill="white"
        textAnchor={x > cx ? 'start' : 'end'}
        dominantBaseline="central"
        fontSize={12}
        fontWeight="bold"
      >
        {`${percentage.toFixed(0)}%`}
      </text>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Contract Status</CardTitle>
        <CardDescription>
          Distribution of contracts by status
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={350}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={renderCustomLabel}
              outerRadius={120}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend
              verticalAlign="bottom"
              height={36}
              formatter={(value, entry: any) => (
                <span style={{ color: entry.color }}>{value}</span>
              )}
            />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}