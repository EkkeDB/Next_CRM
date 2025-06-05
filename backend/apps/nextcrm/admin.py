from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import (
    Cost_Center, Sociedad, Trader, Commodity_Group, Commodity_Type, 
    Commodity, Counterparty, Currency, ExchangeRate, Contract, ContractAmendment
)


@admin.register(Cost_Center)
class CostCenterAdmin(admin.ModelAdmin):
    list_display = ('cost_center_name', 'description', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('cost_center_name', 'description')
    ordering = ('cost_center_name',)


@admin.register(Sociedad)
class SociedadAdmin(admin.ModelAdmin):
    list_display = ('sociedad_name', 'tax_id', 'city', 'country', 'is_active')
    list_filter = ('is_active', 'country', 'created_at')
    search_fields = ('sociedad_name', 'tax_id', 'city')
    ordering = ('sociedad_name',)


@admin.register(Trader)
class TraderAdmin(admin.ModelAdmin):
    list_display = ('trader_name', 'email', 'department', 'is_active', 'hire_date')
    list_filter = ('is_active', 'department', 'hire_date')
    search_fields = ('trader_name', 'email', 'employee_id')
    ordering = ('trader_name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Commodity_Group)
class CommodityGroupAdmin(admin.ModelAdmin):
    list_display = ('commodity_group_name', 'sort_order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('commodity_group_name', 'description')
    ordering = ('sort_order', 'commodity_group_name')


@admin.register(Commodity_Type)
class CommodityTypeAdmin(admin.ModelAdmin):
    list_display = ('commodity_type_name', 'sort_order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('commodity_type_name', 'description')
    ordering = ('sort_order', 'commodity_type_name')


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = ('commodity_name_short', 'commodity_group', 'commodity_type', 'default_unit', 'is_active')
    list_filter = ('commodity_group', 'commodity_type', 'is_active', 'created_at')
    search_fields = ('commodity_name_short', 'commodity_name_full', 'commodity_code')
    ordering = ('commodity_name_short',)


@admin.register(Counterparty)
class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ('counterparty_name', 'counterparty_type', 'city', 'country', 'credit_rating', 'is_active')
    list_filter = ('counterparty_type', 'country', 'credit_rating', 'is_active', 'is_blacklisted')
    search_fields = ('counterparty_name', 'counterparty_code', 'tax_id', 'city')
    ordering = ('counterparty_name',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('counterparty_name', 'counterparty_code', 'tax_id', 'counterparty_type')
        }),
        ('Contact Information', {
            'fields': ('address', 'city', 'state_province', 'postal_code', 'country', 'phone', 'email', 'website')
        }),
        ('Business Information', {
            'fields': ('credit_rating', 'credit_limit', 'payment_terms')
        }),
        ('Primary Contact', {
            'fields': ('primary_contact_name', 'primary_contact_email', 'primary_contact_phone')
        }),
        ('Status', {
            'fields': ('is_active', 'is_blacklisted', 'blacklist_reason')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currency_code', 'currency_name', 'currency_symbol', 'is_base_currency', 'is_active')
    list_filter = ('is_base_currency', 'is_active', 'created_at')
    search_fields = ('currency_code', 'currency_name')
    ordering = ('currency_code',)


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('from_currency', 'to_currency', 'rate', 'rate_date', 'source')
    list_filter = ('from_currency', 'to_currency', 'rate_date', 'source')
    search_fields = ('from_currency__currency_code', 'to_currency__currency_code')
    ordering = ('-rate_date', 'from_currency__currency_code')
    date_hierarchy = 'rate_date'


class ContractAmendmentInline(admin.TabularInline):
    model = ContractAmendment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('amendment_number', 'amendment_type', 'description', 'requested_by', 'approved_by', 'approval_date')


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'counterparty', 'commodity', 'trader', 'status', 'total_value', 'contract_date', 'delivery_status')
    list_filter = ('status', 'commodity__commodity_group', 'trader', 'contract_date', 'delivery_period_start')
    search_fields = ('contract_number', 'counterparty__counterparty_name', 'commodity__commodity_name_short', 'trader__trader_name')
    ordering = ('-contract_date', '-created_at')
    readonly_fields = ('id', 'contract_number', 'total_value', 'created_at', 'updated_at', 'days_to_delivery_display', 'is_overdue_display')
    date_hierarchy = 'contract_date'
    inlines = [ContractAmendmentInline]
    
    fieldsets = (
        ('Contract Identification', {
            'fields': ('id', 'contract_number', 'internal_reference', 'status')
        }),
        ('Parties and Relationships', {
            'fields': ('trader', 'counterparty', 'cost_center', 'sociedad')
        }),
        ('Commodity and Commercial Terms', {
            'fields': ('commodity', 'quantity', 'unit_of_measure', 'price', 'trade_currency', 'total_value')
        }),
        ('Pricing Details', {
            'fields': ('price_basis', 'premium_discount'),
            'classes': ('collapse',)
        }),
        ('Delivery Terms', {
            'fields': ('delivery_terms', 'delivery_location', 'loading_port', 'discharge_port')
        }),
        ('Important Dates', {
            'fields': ('contract_date', 'delivery_period_start', 'delivery_period_end', 'shipment_period_start', 'shipment_period_end')
        }),
        ('Approval Workflow', {
            'fields': ('approval_date', 'approved_by'),
            'classes': ('collapse',)
        }),
        ('Quality and Risk', {
            'fields': ('quality_specifications', 'inspection_terms', 'hedge_required', 'hedge_percentage'),
            'classes': ('collapse',)
        }),
        ('Additional Terms', {
            'fields': ('payment_terms', 'force_majeure_clause', 'special_conditions', 'notes'),
            'classes': ('collapse',)
        }),
        ('Internal Tracking', {
            'fields': ('profit_center',),
            'classes': ('collapse',)
        }),
        ('Status Information', {
            'fields': ('days_to_delivery_display', 'is_overdue_display'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

    def delivery_status(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red;">Overdue</span>')
        elif obj.days_to_delivery is not None:
            if obj.days_to_delivery < 0:
                return format_html('<span style="color: red;">Past due</span>')
            elif obj.days_to_delivery <= 7:
                return format_html('<span style="color: orange;">Due soon ({} days)</span>', obj.days_to_delivery)
            else:
                return format_html('<span style="color: green;">{} days to delivery</span>', obj.days_to_delivery)
        return 'No delivery date'
    delivery_status.short_description = 'Delivery Status'

    def days_to_delivery_display(self, obj):
        return obj.days_to_delivery
    days_to_delivery_display.short_description = 'Days to Delivery'

    def is_overdue_display(self, obj):
        return obj.is_overdue
    is_overdue_display.short_description = 'Is Overdue'
    is_overdue_display.boolean = True

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'trader', 'counterparty', 'commodity', 'trade_currency', 'cost_center', 'sociedad'
        )


@admin.register(ContractAmendment)
class ContractAmendmentAdmin(admin.ModelAdmin):
    list_display = ('contract', 'amendment_number', 'amendment_type', 'requested_by', 'approved_by', 'approval_date', 'created_at')
    list_filter = ('amendment_type', 'approval_date', 'created_at')
    search_fields = ('contract__contract_number', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('contract', 'requested_by', 'approved_by')