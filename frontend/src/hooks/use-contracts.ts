'use client'

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'react-hot-toast'
import apiClient from '@/lib/api'
import { QUERY_KEYS, TOAST_MESSAGES } from '@/lib/constants'
import { getErrorMessage } from '@/lib/utils'
import type { Contract, ContractFilters, ContractFormData, ApiResponse } from '@/types'

// Get all contracts with filters
export function useContracts(filters?: ContractFilters) {
  return useQuery({
    queryKey: [QUERY_KEYS.CONTRACTS, filters],
    queryFn: () => apiClient.getContracts(filters),
    staleTime: 30 * 1000, // 30 seconds
  })
}

// Get single contract
export function useContract(id: string) {
  return useQuery({
    queryKey: [QUERY_KEYS.CONTRACT, id],
    queryFn: () => apiClient.getContract(id),
    enabled: !!id,
  })
}

// Create contract mutation
export function useCreateContract() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: ContractFormData) => apiClient.createContract(data),
    onSuccess: (data) => {
      // Invalidate contracts list
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.CONTRACTS] })
      // Invalidate dashboard stats
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.DASHBOARD_STATS] })
      toast.success(TOAST_MESSAGES.SUCCESS.CONTRACT_CREATED)
    },
    onError: (error) => {
      const message = getErrorMessage(error)
      toast.error(message || TOAST_MESSAGES.ERROR.GENERIC)
    },
  })
}

// Update contract mutation
export function useUpdateContract() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<ContractFormData> }) =>
      apiClient.updateContract(id, data),
    onSuccess: (data, variables) => {
      // Update contract in cache
      queryClient.setQueryData([QUERY_KEYS.CONTRACT, variables.id], data)
      // Invalidate contracts list
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.CONTRACTS] })
      // Invalidate dashboard stats
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.DASHBOARD_STATS] })
      toast.success(TOAST_MESSAGES.SUCCESS.CONTRACT_UPDATED)
    },
    onError: (error) => {
      const message = getErrorMessage(error)
      toast.error(message || TOAST_MESSAGES.ERROR.GENERIC)
    },
  })
}

// Delete contract mutation
export function useDeleteContract() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => apiClient.deleteContract(id),
    onSuccess: (_, id) => {
      // Remove contract from cache
      queryClient.removeQueries({ queryKey: [QUERY_KEYS.CONTRACT, id] })
      // Invalidate contracts list
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.CONTRACTS] })
      // Invalidate dashboard stats
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.DASHBOARD_STATS] })
      toast.success('Contract deleted successfully')
    },
    onError: (error) => {
      const message = getErrorMessage(error)
      toast.error(message || TOAST_MESSAGES.ERROR.GENERIC)
    },
  })
}

// Approve contract mutation
export function useApproveContract() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => apiClient.approveContract(id),
    onSuccess: (_, id) => {
      // Invalidate contract data
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.CONTRACT, id] })
      // Invalidate contracts list
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.CONTRACTS] })
      // Invalidate dashboard stats
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.DASHBOARD_STATS] })
      toast.success(TOAST_MESSAGES.SUCCESS.CONTRACT_APPROVED)
    },
    onError: (error) => {
      const message = getErrorMessage(error)
      toast.error(message || TOAST_MESSAGES.ERROR.GENERIC)
    },
  })
}

// Cancel contract mutation
export function useCancelContract() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, reason }: { id: string; reason?: string }) =>
      apiClient.cancelContract(id, reason),
    onSuccess: (_, variables) => {
      // Invalidate contract data
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.CONTRACT, variables.id] })
      // Invalidate contracts list
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.CONTRACTS] })
      // Invalidate dashboard stats
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.DASHBOARD_STATS] })
      toast.success(TOAST_MESSAGES.SUCCESS.CONTRACT_CANCELLED)
    },
    onError: (error) => {
      const message = getErrorMessage(error)
      toast.error(message || TOAST_MESSAGES.ERROR.GENERIC)
    },
  })
}