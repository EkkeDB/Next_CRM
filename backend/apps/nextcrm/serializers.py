from rest_framework import serializers
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Cost_Center, Sociedad, Trader, Commodity_Group, Commodity_Type,
    Commodity, Counterparty, Currency, ExchangeRate, Contract, ContractAmendment
)


class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cost_Center
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class SociedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sociedad
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class TraderSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='trader_name', read_only=True)
    
    class Meta:
        model = Trader
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CommodityGroupSerializer(serializers.ModelSerializer):
    commodities_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Commodity_Group
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_commodities_count(self, obj):
        return obj.commodities.filter(is_active=True).count()


class CommodityTypeSerializer(serializers.ModelSerializer):
    commodities_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Commodity_Type
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_commodities_count(self, obj):
        return obj.commodities.filter(is_active=True).count()


class CommoditySerializer(serializers.ModelSerializer):
    commodity_group_name = serializers.CharField(source='commodity_group.commodity_group_name', read_only=True)
    commodity_type_name = serializers.CharField(source='commodity_type.commodity_type_name', read_only=True)
    active_contracts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Commodity
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_active_contracts_count(self, obj):
        return obj.contracts.filter(status__in=['approved', 'executed', 'partially_executed']).count()


class CounterpartySerializer(serializers.ModelSerializer):
    contracts_count = serializers.SerializerMethodField()
    total_contract_value = serializers.SerializerMethodField()
    last_contract_date = serializers.SerializerMethodField()
    
    class Meta:
        model = Counterparty
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_contracts_count(self, obj):
        return obj.contracts.count()
    
    def get_total_contract_value(self, obj):
        total = obj.contracts.aggregate(total=Sum('total_value'))['total']
        return total or 0
    
    def get_last_contract_date(self, obj):
        last_contract = obj.contracts.order_by('-contract_date').first()
        return last_contract.contract_date if last_contract else None


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ExchangeRateSerializer(serializers.ModelSerializer):
    from_currency_code = serializers.CharField(source='from_currency.currency_code', read_only=True)
    to_currency_code = serializers.CharField(source='to_currency.currency_code', read_only=True)
    
    class Meta:
        model = ExchangeRate
        fields = '__all__'
        read_only_fields = ('created_at',)


class ContractListSerializer(serializers.ModelSerializer):
    trader_name = serializers.CharField(source='trader.trader_name', read_only=True)
    counterparty_name = serializers.CharField(source='counterparty.counterparty_name', read_only=True)
    commodity_name = serializers.CharField(source='commodity.commodity_name_short', read_only=True)
    currency_code = serializers.CharField(source='trade_currency.currency_code', read_only=True)
    days_to_delivery = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    completion_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Contract
        fields = [
            'id', 'contract_number', 'trader_name', 'counterparty_name', 'commodity_name',
            'quantity', 'unit_of_measure', 'price', 'currency_code', 'total_value',
            'contract_date', 'delivery_period_start', 'delivery_period_end', 'status',
            'days_to_delivery', 'is_overdue', 'completion_percentage', 'created_at'
        ]


class ContractDetailSerializer(serializers.ModelSerializer):
    trader_name = serializers.CharField(source='trader.trader_name', read_only=True)
    counterparty_name = serializers.CharField(source='counterparty.counterparty_name', read_only=True)
    commodity_name = serializers.CharField(source='commodity.commodity_name_short', read_only=True)
    commodity_group_name = serializers.CharField(source='commodity.commodity_group.commodity_group_name', read_only=True)
    currency_code = serializers.CharField(source='trade_currency.currency_code', read_only=True)
    cost_center_name = serializers.CharField(source='cost_center.cost_center_name', read_only=True)
    sociedad_name = serializers.CharField(source='sociedad.sociedad_name', read_only=True)
    
    days_to_delivery = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    completion_percentage = serializers.ReadOnlyField()
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    updated_by_username = serializers.CharField(source='updated_by.username', read_only=True)
    approved_by_username = serializers.CharField(source='approved_by.username', read_only=True)
    
    amendments = serializers.SerializerMethodField()
    
    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ('id', 'contract_number', 'total_value', 'created_at', 'updated_at')
    
    def get_amendments(self, obj):
        amendments = obj.amendments.all()[:5]  # Last 5 amendments
        return ContractAmendmentSerializer(amendments, many=True).data


class ContractCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            'trader', 'counterparty', 'commodity', 'cost_center', 'sociedad',
            'quantity', 'unit_of_measure', 'price', 'trade_currency',
            'price_basis', 'premium_discount',
            'delivery_terms', 'delivery_location', 'loading_port', 'discharge_port',
            'contract_date', 'delivery_period_start', 'delivery_period_end',
            'shipment_period_start', 'shipment_period_end',
            'quality_specifications', 'inspection_terms',
            'hedge_required', 'hedge_percentage',
            'payment_terms', 'force_majeure_clause', 'special_conditions', 'notes',
            'internal_reference', 'profit_center'
        ]
    
    def validate(self, data):
        # Validate delivery dates
        if data.get('delivery_period_start') and data.get('delivery_period_end'):
            if data['delivery_period_start'] > data['delivery_period_end']:
                raise serializers.ValidationError(
                    "Delivery period start must be before delivery period end"
                )
        
        # Validate shipment dates if provided
        if data.get('shipment_period_start') and data.get('shipment_period_end'):
            if data['shipment_period_start'] > data['shipment_period_end']:
                raise serializers.ValidationError(
                    "Shipment period start must be before shipment period end"
                )
        
        # Validate hedge percentage
        if data.get('hedge_percentage', 0) > 100:
            raise serializers.ValidationError("Hedge percentage cannot exceed 100%")
        
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['updated_by'] = request.user
        return super().update(instance, validated_data)


class ContractAmendmentSerializer(serializers.ModelSerializer):
    requested_by_username = serializers.CharField(source='requested_by.username', read_only=True)
    approved_by_username = serializers.CharField(source='approved_by.username', read_only=True)
    
    class Meta:
        model = ContractAmendment
        fields = '__all__'
        read_only_fields = ('created_at',)
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['requested_by'] = request.user
        return super().create(validated_data)


class DashboardStatsSerializer(serializers.Serializer):
    total_contracts = serializers.IntegerField()
    active_contracts = serializers.IntegerField()
    completed_contracts = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=18, decimal_places=2)
    total_counterparties = serializers.IntegerField()
    overdue_contracts = serializers.IntegerField()
    
    # Monthly data for charts
    monthly_contracts = serializers.ListField()
    monthly_revenue = serializers.ListField()
    status_distribution = serializers.DictField()
    top_commodities = serializers.ListField()
    top_counterparties = serializers.ListField()
    upcoming_deliveries = serializers.ListField()


class MonthlyStatsSerializer(serializers.Serializer):
    month = serializers.CharField()
    contracts_count = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=18, decimal_places=2)


class StatusDistributionSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.FloatField()


class TopCommoditySerializer(serializers.Serializer):
    commodity_name = serializers.CharField()
    contracts_count = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=18, decimal_places=2)


class TopCounterpartySerializer(serializers.Serializer):
    counterparty_name = serializers.CharField()
    contracts_count = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=18, decimal_places=2)


class UpcomingDeliverySerializer(serializers.Serializer):
    contract_number = serializers.CharField()
    counterparty_name = serializers.CharField()
    commodity_name = serializers.CharField()
    delivery_date = serializers.DateField()
    days_remaining = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=18, decimal_places=2)