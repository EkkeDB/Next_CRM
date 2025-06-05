'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Eye, Edit, MoreHorizontal, CheckCircle, XCircle } from 'lucide-react'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useContracts, useApproveContract, useCancelContract } from '@/hooks/use-contracts'
import { formatDate, formatCurrency, getContractStatusColor, cn } from '@/lib/utils'
import type { ContractFilters, Contract } from '@/types'

interface ContractsTableProps {
  filters?: ContractFilters
}

export function ContractsTable({ filters }: ContractsTableProps) {
  const { data, isLoading, error } = useContracts(filters)
  const approveContract = useApproveContract()
  const cancelContract = useCancelContract()
  const [selectedContracts, setSelectedContracts] = useState<string[]>([])

  const handleApprove = async (contractId: string, e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    try {
      await approveContract.mutateAsync(contractId)
    } catch (error) {
      console.error('Failed to approve contract:', error)
    }
  }

  const handleCancel = async (contractId: string, e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    
    const reason = prompt('Please provide a reason for cancelling this contract:')
    if (reason !== null) {
      try {
        await cancelContract.mutateAsync({ id: contractId, reason })
      } catch (error) {
        console.error('Failed to cancel contract:', error)
      }
    }
  }

  const toggleContract = (contractId: string) => {
    setSelectedContracts(prev => 
      prev.includes(contractId)
        ? prev.filter(id => id !== contractId)
        : [...prev, contractId]
    )
  }

  const toggleAll = () => {
    if (!data?.results) return
    
    if (selectedContracts.length === data.results.length) {
      setSelectedContracts([])
    } else {
      setSelectedContracts(data.results.map(contract => contract.id))
    }
  }

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Contracts</CardTitle>
          <CardDescription>Loading contracts...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="h-12 bg-muted rounded animate-pulse" />
            ))}
          </div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Contracts</CardTitle>
          <CardDescription>Failed to load contracts</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-muted-foreground">
            Unable to load contracts. Please try again.
          </div>
        </CardContent>
      </Card>
    )
  }

  if (!data?.results || data.results.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Contracts</CardTitle>
          <CardDescription>No contracts found</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-muted-foreground">
            <div className="mb-4">
              <svg
                className="mx-auto h-12 w-12 opacity-50"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <p>No contracts match your current filters.</p>
            <Button asChild className="mt-4">
              <Link href="/contracts/new">Create New Contract</Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Contracts</CardTitle>
            <CardDescription>
              {data.count} contract{data.count !== 1 ? 's' : ''} found
            </CardDescription>
          </div>
          <Button asChild>
            <Link href="/contracts/new">Create Contract</Link>
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-12">
                <input
                  type="checkbox"
                  checked={selectedContracts.length === data.results.length}
                  onChange={toggleAll}
                  className="rounded border-gray-300"
                />
              </TableHead>
              <TableHead>Contract #</TableHead>
              <TableHead>Counterparty</TableHead>
              <TableHead>Commodity</TableHead>
              <TableHead>Quantity</TableHead>
              <TableHead>Value</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Delivery</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.results.map((contract) => (
              <TableRow
                key={contract.id}
                className={cn(
                  'cursor-pointer hover:bg-muted/50',
                  selectedContracts.includes(contract.id) && 'bg-muted/30'
                )}
                onClick={() => toggleContract(contract.id)}
              >
                <TableCell>
                  <input
                    type="checkbox"
                    checked={selectedContracts.includes(contract.id)}
                    onChange={() => toggleContract(contract.id)}
                    className="rounded border-gray-300"
                    onClick={e => e.stopPropagation()}
                  />
                </TableCell>
                
                <TableCell className="font-medium">
                  <Link
                    href={`/contracts/${contract.id}`}
                    className="text-primary hover:underline"
                    onClick={e => e.stopPropagation()}
                  >
                    {contract.contract_number}
                  </Link>
                </TableCell>
                
                <TableCell>
                  <div>
                    <div className="font-medium">{contract.counterparty_name}</div>
                    <div className="text-sm text-muted-foreground">
                      {contract.trader_name}
                    </div>
                  </div>
                </TableCell>
                
                <TableCell>
                  <div>
                    <div className="font-medium">{contract.commodity_name}</div>
                    <div className="text-sm text-muted-foreground">
                      {contract.commodity_group_name}
                    </div>
                  </div>
                </TableCell>
                
                <TableCell>
                  {contract.quantity?.toLocaleString()} {contract.unit_of_measure}
                </TableCell>
                
                <TableCell className="font-medium">
                  {formatCurrency(contract.total_value || 0)} {contract.currency_code}
                </TableCell>
                
                <TableCell>
                  <Badge className={getContractStatusColor(contract.status)}>
                    {contract.status.replace('_', ' ').toUpperCase()}
                  </Badge>
                </TableCell>
                
                <TableCell>
                  <div>
                    <div className="text-sm">
                      {formatDate(contract.delivery_period_start)}
                    </div>
                    {contract.days_to_delivery !== null && (
                      <div className={cn(
                        'text-xs',
                        contract.is_overdue 
                          ? 'text-red-600' 
                          : contract.days_to_delivery <= 7
                          ? 'text-orange-600'
                          : 'text-muted-foreground'
                      )}>
                        {contract.is_overdue 
                          ? 'Overdue'
                          : `${contract.days_to_delivery}d remaining`
                        }
                      </div>
                    )}
                  </div>
                </TableCell>
                
                <TableCell>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="ghost"
                      size="icon"
                      asChild
                      onClick={e => e.stopPropagation()}
                    >
                      <Link href={`/contracts/${contract.id}`}>
                        <Eye className="h-4 w-4" />
                      </Link>
                    </Button>
                    
                    <Button
                      variant="ghost"
                      size="icon"
                      asChild
                      onClick={e => e.stopPropagation()}
                    >
                      <Link href={`/contracts/${contract.id}/edit`}>
                        <Edit className="h-4 w-4" />
                      </Link>
                    </Button>
                    
                    {contract.status === 'draft' && (
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={(e) => handleApprove(contract.id, e)}
                        disabled={approveContract.isPending}
                        title="Approve Contract"
                      >
                        <CheckCircle className="h-4 w-4 text-green-600" />
                      </Button>
                    )}
                    
                    {contract.status !== 'completed' && contract.status !== 'cancelled' && (
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={(e) => handleCancel(contract.id, e)}
                        disabled={cancelContract.isPending}
                        title="Cancel Contract"
                      >
                        <XCircle className="h-4 w-4 text-red-600" />
                      </Button>
                    )}
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        
        {/* Pagination would go here */}
        {data.next || data.previous ? (
          <div className="flex items-center justify-between mt-4">
            <div className="text-sm text-muted-foreground">
              Showing {data.results.length} of {data.count} contracts
            </div>
            <div className="flex gap-2">
              {data.previous && (
                <Button variant="outline" size="sm">
                  Previous
                </Button>
              )}
              {data.next && (
                <Button variant="outline" size="sm">
                  Next
                </Button>
              )}
            </div>
          </div>
        ) : null}
      </CardContent>
    </Card>
  )
}