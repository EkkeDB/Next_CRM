'use client'

import {
  FileText,
  CheckCircle,
  AlertTriangle,
  DollarSign,
  Users,
  TrendingUp,
} from 'lucide-react'
import { StatCard } from '@/components/ui/stat-card'
import { useDashboardStats } from '@/hooks/use-dashboard'
import { formatCurrency } from '@/lib/utils'

export function DashboardStats() {
  const { data: stats, isLoading, error } = useDashboardStats()

  if (isLoading) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-6">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="h-32 bg-muted rounded-lg animate-pulse" />
        ))}
      </div>
    )
  }

  if (error || !stats) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-6">
        <div className="col-span-full text-center py-8 text-muted-foreground">
          Failed to load dashboard statistics
        </div>
      </div>
    )
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-6">
      <StatCard
        title="Total Contracts"
        value={stats.total_contracts}
        description="All time"
        icon={FileText}
        format="number"
      />
      
      <StatCard
        title="Active Contracts"
        value={stats.active_contracts}
        description="Currently active"
        icon={TrendingUp}
        format="number"
      />
      
      <StatCard
        title="Completed"
        value={stats.completed_contracts}
        description="Successfully completed"
        icon={CheckCircle}
        format="number"
      />
      
      <StatCard
        title="Total Value"
        value={stats.total_value}
        description="Contract portfolio"
        icon={DollarSign}
        format="currency"
      />
      
      <StatCard
        title="Counterparties"
        value={stats.total_counterparties}
        description="Active partners"
        icon={Users}
        format="number"
      />
      
      <StatCard
        title="Overdue"
        value={stats.overdue_contracts}
        description="Require attention"
        icon={AlertTriangle}
        format="number"
        className={stats.overdue_contracts > 0 ? 'border-orange-200 bg-orange-50' : ''}
      />
    </div>
  )
}