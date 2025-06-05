from rest_framework import generics, viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Cost_Center, Sociedad, Trader, Commodity_Group, Commodity_Type,
    Commodity, Counterparty, Currency, ExchangeRate, Contract, ContractAmendment
)
from .serializers import (
    CostCenterSerializer, SociedadSerializer, TraderSerializer,
    CommodityGroupSerializer, CommodityTypeSerializer, CommoditySerializer,
    CounterpartySerializer, CurrencySerializer, ExchangeRateSerializer,
    ContractListSerializer, ContractDetailSerializer, ContractCreateUpdateSerializer,
    ContractAmendmentSerializer, DashboardStatsSerializer
)
from apps.authentication.utils import log_audit_event


class CostCenterViewSet(viewsets.ModelViewSet):
    queryset = Cost_Center.objects.filter(is_active=True)
    serializer_class = CostCenterSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['cost_center_name', 'description']
    ordering_fields = ['cost_center_name', 'created_at']
    ordering = ['cost_center_name']


class SociedadViewSet(viewsets.ModelViewSet):
    queryset = Sociedad.objects.filter(is_active=True)
    serializer_class = SociedadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['sociedad_name', 'tax_id', 'city', 'country']
    ordering_fields = ['sociedad_name', 'created_at']
    ordering = ['sociedad_name']


class TraderViewSet(viewsets.ModelViewSet):
    queryset = Trader.objects.filter(is_active=True)
    serializer_class = TraderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['trader_name', 'email', 'employee_id']
    ordering_fields = ['trader_name', 'created_at']
    ordering = ['trader_name']


class CommodityGroupViewSet(viewsets.ModelViewSet):
    queryset = Commodity_Group.objects.filter(is_active=True)
    serializer_class = CommodityGroupSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['commodity_group_name', 'description']
    ordering_fields = ['sort_order', 'commodity_group_name']
    ordering = ['sort_order', 'commodity_group_name']


class CommodityTypeViewSet(viewsets.ModelViewSet):
    queryset = Commodity_Type.objects.filter(is_active=True)
    serializer_class = CommodityTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['commodity_type_name', 'description']
    ordering_fields = ['sort_order', 'commodity_type_name']
    ordering = ['sort_order', 'commodity_type_name']


class CommodityViewSet(viewsets.ModelViewSet):
    queryset = Commodity.objects.filter(is_active=True).select_related('commodity_group', 'commodity_type')
    serializer_class = CommoditySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['commodity_group', 'commodity_type']
    search_fields = ['commodity_name_short', 'commodity_name_full', 'commodity_code']
    ordering_fields = ['commodity_name_short', 'created_at']
    ordering = ['commodity_name_short']


class CounterpartyViewSet(viewsets.ModelViewSet):
    queryset = Counterparty.objects.filter(is_active=True)
    serializer_class = CounterpartySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['counterparty_type', 'country', 'credit_rating']
    search_fields = ['counterparty_name', 'counterparty_code', 'city']
    ordering_fields = ['counterparty_name', 'created_at']
    ordering = ['counterparty_name']
    
    def perform_create(self, serializer):
        instance = serializer.save()
        log_audit_event(self.request, 'CREATE', 'Counterparty', instance.id, str(instance))
    
    def perform_update(self, serializer):
        instance = serializer.save()
        log_audit_event(self.request, 'UPDATE', 'Counterparty', instance.id, str(instance))


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.filter(is_active=True)
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['currency_code', 'currency_name']
    ordering_fields = ['currency_code', 'created_at']
    ordering = ['currency_code']


class ExchangeRateViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRate.objects.all().select_related('from_currency', 'to_currency')
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['from_currency', 'to_currency', 'rate_date']
    ordering_fields = ['rate_date', 'from_currency__currency_code']
    ordering = ['-rate_date']


class ContractViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'trader', 'counterparty', 'commodity__commodity_group', 'contract_date']
    search_fields = ['contract_number', 'counterparty__counterparty_name', 'commodity__commodity_name_short']
    ordering_fields = ['contract_date', 'total_value', 'delivery_period_start', 'created_at']
    ordering = ['-contract_date', '-created_at']
    
    def get_queryset(self):
        return Contract.objects.select_related(
            'trader', 'counterparty', 'commodity', 'commodity__commodity_group',
            'trade_currency', 'cost_center', 'sociedad'
        ).prefetch_related('amendments')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ContractListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ContractCreateUpdateSerializer
        return ContractDetailSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        log_audit_event(self.request, 'CREATE', 'Contract', str(instance.id), str(instance))
    
    def perform_update(self, serializer):
        instance = serializer.save()
        log_audit_event(self.request, 'UPDATE', 'Contract', str(instance.id), str(instance))
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        contract = self.get_object()
        if contract.status != 'draft' and contract.status != 'pending_approval':
            return Response(
                {'error': 'Only draft or pending approval contracts can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        contract.status = 'approved'
        contract.approval_date = timezone.now()
        contract.approved_by = request.user
        contract.save()
        
        log_audit_event(request, 'UPDATE', 'Contract', str(contract.id), f'Contract approved: {contract}')
        
        return Response({'message': 'Contract approved successfully'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        contract = self.get_object()
        if contract.status in ['completed', 'cancelled']:
            return Response(
                {'error': 'Cannot cancel completed or already cancelled contracts'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reason = request.data.get('reason', '')
        contract.status = 'cancelled'
        if reason:
            contract.notes = f"{contract.notes}\n\nCancelled: {reason}".strip()
        contract.save()
        
        log_audit_event(request, 'UPDATE', 'Contract', str(contract.id), f'Contract cancelled: {contract}')
        
        return Response({'message': 'Contract cancelled successfully'})
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        stats = get_dashboard_statistics()
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)


class ContractAmendmentViewSet(viewsets.ModelViewSet):
    serializer_class = ContractAmendmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['contract', 'amendment_type', 'approval_date']
    ordering_fields = ['created_at', 'approval_date']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return ContractAmendment.objects.select_related('contract', 'requested_by', 'approved_by')
    
    def perform_create(self, serializer):
        instance = serializer.save()
        log_audit_event(self.request, 'CREATE', 'ContractAmendment', instance.id, str(instance))
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        amendment = self.get_object()
        if amendment.approval_date:
            return Response(
                {'error': 'Amendment already approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        amendment.approved_by = request.user
        amendment.approval_date = timezone.now()
        amendment.save()
        
        log_audit_event(request, 'UPDATE', 'ContractAmendment', amendment.id, f'Amendment approved: {amendment}')
        
        return Response({'message': 'Amendment approved successfully'})


def get_dashboard_statistics():
    """Calculate dashboard statistics"""
    now = timezone.now()
    current_year = now.year
    current_month = now.month
    
    # Basic counts
    total_contracts = Contract.objects.count()
    active_contracts = Contract.objects.filter(
        status__in=['approved', 'executed', 'partially_executed']
    ).count()
    completed_contracts = Contract.objects.filter(status='completed').count()
    total_counterparties = Counterparty.objects.filter(is_active=True).count()
    
    # Overdue contracts
    overdue_contracts = Contract.objects.filter(
        delivery_period_end__lt=now.date(),
        status__in=['approved', 'executed', 'partially_executed']
    ).count()
    
    # Total value (in base currency)
    total_value_agg = Contract.objects.aggregate(total=Sum('total_value'))
    total_value = total_value_agg['total'] or 0
    
    # Monthly contracts for the last 12 months
    monthly_contracts = []
    monthly_revenue = []
    
    for i in range(12):
        month_date = now.replace(day=1) - timedelta(days=i*30)
        month_start = month_date.replace(day=1)
        if month_date.month == 12:
            month_end = month_date.replace(year=month_date.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = month_date.replace(month=month_date.month + 1, day=1) - timedelta(days=1)
        
        contracts_count = Contract.objects.filter(
            contract_date__range=[month_start, month_end]
        ).count()
        
        revenue = Contract.objects.filter(
            contract_date__range=[month_start, month_end]
        ).aggregate(total=Sum('total_value'))['total'] or 0
        
        monthly_contracts.insert(0, {
            'month': month_date.strftime('%Y-%m'),
            'contracts_count': contracts_count
        })
        
        monthly_revenue.insert(0, {
            'month': month_date.strftime('%Y-%m'),
            'total_value': float(revenue)
        })
    
    # Status distribution
    status_counts = Contract.objects.values('status').annotate(count=Count('id'))
    status_distribution = {}
    for item in status_counts:
        status_distribution[item['status']] = {
            'count': item['count'],
            'percentage': round((item['count'] / total_contracts) * 100, 2) if total_contracts > 0 else 0
        }
    
    # Top commodities
    top_commodities = Contract.objects.values(
        'commodity__commodity_name_short'
    ).annotate(
        contracts_count=Count('id'),
        total_value=Sum('total_value')
    ).order_by('-total_value')[:5]
    
    top_commodities_list = []
    for item in top_commodities:
        top_commodities_list.append({
            'commodity_name': item['commodity__commodity_name_short'],
            'contracts_count': item['contracts_count'],
            'total_value': float(item['total_value'] or 0)
        })
    
    # Top counterparties
    top_counterparties = Contract.objects.values(
        'counterparty__counterparty_name'
    ).annotate(
        contracts_count=Count('id'),
        total_value=Sum('total_value')
    ).order_by('-total_value')[:5]
    
    top_counterparties_list = []
    for item in top_counterparties:
        top_counterparties_list.append({
            'counterparty_name': item['counterparty__counterparty_name'],
            'contracts_count': item['contracts_count'],
            'total_value': float(item['total_value'] or 0)
        })
    
    # Upcoming deliveries (next 30 days)
    upcoming_deliveries = Contract.objects.filter(
        delivery_period_start__lte=now.date() + timedelta(days=30),
        delivery_period_start__gte=now.date(),
        status__in=['approved', 'executed', 'partially_executed']
    ).select_related('counterparty', 'commodity').order_by('delivery_period_start')[:10]
    
    upcoming_deliveries_list = []
    for contract in upcoming_deliveries:
        days_remaining = (contract.delivery_period_start - now.date()).days
        upcoming_deliveries_list.append({
            'contract_number': contract.contract_number,
            'counterparty_name': contract.counterparty.counterparty_name,
            'commodity_name': contract.commodity.commodity_name_short,
            'delivery_date': contract.delivery_period_start,
            'days_remaining': days_remaining,
            'total_value': float(contract.total_value or 0)
        })
    
    return {
        'total_contracts': total_contracts,
        'active_contracts': active_contracts,
        'completed_contracts': completed_contracts,
        'total_value': total_value,
        'total_counterparties': total_counterparties,
        'overdue_contracts': overdue_contracts,
        'monthly_contracts': monthly_contracts,
        'monthly_revenue': monthly_revenue,
        'status_distribution': status_distribution,
        'top_commodities': top_commodities_list,
        'top_counterparties': top_counterparties_list,
        'upcoming_deliveries': upcoming_deliveries_list
    }


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_global(request):
    """Global search across all entities"""
    query = request.GET.get('q', '').strip()
    if not query or len(query) < 2:
        return Response({'error': 'Query must be at least 2 characters'}, status=400)
    
    results = {
        'contracts': [],
        'counterparties': [],
        'commodities': [],
        'traders': []
    }
    
    # Search contracts
    contracts = Contract.objects.filter(
        Q(contract_number__icontains=query) |
        Q(counterparty__counterparty_name__icontains=query) |
        Q(commodity__commodity_name_short__icontains=query)
    ).select_related('counterparty', 'commodity')[:5]
    
    for contract in contracts:
        results['contracts'].append({
            'id': str(contract.id),
            'contract_number': contract.contract_number,
            'counterparty_name': contract.counterparty.counterparty_name,
            'commodity_name': contract.commodity.commodity_name_short,
            'total_value': float(contract.total_value or 0),
            'status': contract.status
        })
    
    # Search counterparties
    counterparties = Counterparty.objects.filter(
        Q(counterparty_name__icontains=query) |
        Q(counterparty_code__icontains=query)
    ).filter(is_active=True)[:5]
    
    for cp in counterparties:
        results['counterparties'].append({
            'id': cp.id,
            'counterparty_name': cp.counterparty_name,
            'counterparty_type': cp.counterparty_type,
            'city': cp.city,
            'country': cp.country
        })
    
    # Search commodities
    commodities = Commodity.objects.filter(
        Q(commodity_name_short__icontains=query) |
        Q(commodity_name_full__icontains=query)
    ).filter(is_active=True)[:5]
    
    for commodity in commodities:
        results['commodities'].append({
            'id': commodity.id,
            'commodity_name_short': commodity.commodity_name_short,
            'commodity_name_full': commodity.commodity_name_full,
            'commodity_group': commodity.commodity_group.commodity_group_name
        })
    
    # Search traders
    traders = Trader.objects.filter(
        Q(trader_name__icontains=query) |
        Q(email__icontains=query)
    ).filter(is_active=True)[:5]
    
    for trader in traders:
        results['traders'].append({
            'id': trader.id,
            'trader_name': trader.trader_name,
            'email': trader.email,
            'department': trader.department
        })
    
    return Response(results)