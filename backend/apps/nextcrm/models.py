from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid


class Cost_Center(models.Model):
    cost_center_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['cost_center_name']
        verbose_name = 'Cost Center'
        verbose_name_plural = 'Cost Centers'

    def __str__(self):
        return self.cost_center_name


class Sociedad(models.Model):
    sociedad_name = models.CharField(max_length=50, unique=True)
    tax_id = models.CharField(max_length=20, unique=True, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sociedad_name']
        verbose_name = 'Sociedad'
        verbose_name_plural = 'Sociedades'

    def __str__(self):
        return self.sociedad_name


class Trader(models.Model):
    trader_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    department = models.CharField(max_length=50, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='trader_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['trader_name']

    def __str__(self):
        return self.trader_name


class Commodity_Group(models.Model):
    commodity_group_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'commodity_group_name']
        verbose_name = 'Commodity Group'
        verbose_name_plural = 'Commodity Groups'

    def __str__(self):
        return self.commodity_group_name


class Commodity_Type(models.Model):
    commodity_type_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'commodity_type_name']
        verbose_name = 'Commodity Type'
        verbose_name_plural = 'Commodity Types'

    def __str__(self):
        return self.commodity_type_name


class Commodity(models.Model):
    commodity_name_short = models.CharField(max_length=50, unique=True)
    commodity_name_full = models.CharField(max_length=200, blank=True)
    commodity_group = models.ForeignKey(Commodity_Group, on_delete=models.CASCADE, related_name='commodities')
    commodity_type = models.ForeignKey(Commodity_Type, on_delete=models.CASCADE, related_name='commodities')
    commodity_code = models.CharField(max_length=20, unique=True, blank=True)
    default_unit = models.CharField(max_length=20, default='MT')
    quality_specifications = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['commodity_name_short']
        verbose_name = 'Commodity'
        verbose_name_plural = 'Commodities'

    def __str__(self):
        return f"{self.commodity_name_short} - {self.commodity_group}"


class Counterparty(models.Model):
    COUNTERPARTY_TYPES = [
        ('supplier', 'Supplier'),
        ('customer', 'Customer'),
        ('both', 'Both'),
    ]
    
    RATING_CHOICES = [
        ('AAA', 'AAA'),
        ('AA', 'AA'),
        ('A', 'A'),
        ('BBB', 'BBB'),
        ('BB', 'BB'),
        ('B', 'B'),
        ('CCC', 'CCC'),
        ('CC', 'CC'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    counterparty_name = models.CharField(max_length=100)
    counterparty_code = models.CharField(max_length=20, unique=True, blank=True)
    tax_id = models.CharField(max_length=30, blank=True)
    
    # Contact Information
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state_province = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    
    # Business Information
    counterparty_type = models.CharField(max_length=10, choices=COUNTERPARTY_TYPES, default='customer')
    credit_rating = models.CharField(max_length=3, choices=RATING_CHOICES, blank=True)
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    payment_terms = models.CharField(max_length=50, blank=True)
    
    # Contact Persons
    primary_contact_name = models.CharField(max_length=100, blank=True)
    primary_contact_email = models.EmailField(blank=True)
    primary_contact_phone = models.CharField(max_length=20, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_blacklisted = models.BooleanField(default=False)
    blacklist_reason = models.TextField(blank=True)
    
    # Metadata
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['counterparty_name']
        verbose_name = 'Counterparty'
        verbose_name_plural = 'Counterparties'

    def __str__(self):
        return f"{self.counterparty_name} ({self.counterparty_type})"

    @property
    def is_supplier(self):
        return self.counterparty_type in ['supplier', 'both']

    @property
    def is_customer(self):
        return self.counterparty_type in ['customer', 'both']


class Currency(models.Model):
    currency_code = models.CharField(max_length=3, unique=True)  # ISO 4217
    currency_name = models.CharField(max_length=50)
    currency_symbol = models.CharField(max_length=5, blank=True)
    is_base_currency = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    decimal_places = models.IntegerField(default=2, validators=[MinValueValidator(0), MaxValueValidator(4)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['currency_code']
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return f"{self.currency_code} - {self.currency_name}"


class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='from_rates')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='to_rates')
    rate = models.DecimalField(max_digits=15, decimal_places=6)
    rate_date = models.DateField()
    source = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rate_date']
        unique_together = ['from_currency', 'to_currency', 'rate_date']

    def __str__(self):
        return f"{self.from_currency.currency_code}/{self.to_currency.currency_code} = {self.rate} ({self.rate_date})"


class Contract(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('executed', 'Executed'),
        ('partially_executed', 'Partially Executed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    DELIVERY_TERMS = [
        ('FOB', 'Free on Board'),
        ('CIF', 'Cost, Insurance, and Freight'),
        ('CFR', 'Cost and Freight'),
        ('EXW', 'Ex Works'),
        ('FCA', 'Free Carrier'),
        ('CPT', 'Carriage Paid To'),
        ('CIP', 'Carriage and Insurance Paid To'),
        ('DAP', 'Delivered at Place'),
        ('DPU', 'Delivered at Place Unloaded'),
        ('DDP', 'Delivered Duty Paid'),
    ]

    # Auto-generated fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract_number = models.CharField(max_length=50, unique=True, blank=True)
    
    # Core relationships
    trader = models.ForeignKey(Trader, on_delete=models.PROTECT, related_name='contracts')
    counterparty = models.ForeignKey(Counterparty, on_delete=models.PROTECT, related_name='contracts')
    commodity = models.ForeignKey(Commodity, on_delete=models.PROTECT, related_name='contracts')
    cost_center = models.ForeignKey(Cost_Center, on_delete=models.PROTECT, related_name='contracts', null=True, blank=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT, related_name='contracts', null=True, blank=True)
    
    # Commercial terms
    quantity = models.DecimalField(max_digits=15, decimal_places=3, default=0, validators=[MinValueValidator(Decimal('0.001'))])
    unit_of_measure = models.CharField(max_length=20, default='MT')
    price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    trade_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='contracts')
    
    # Pricing details
    price_basis = models.CharField(max_length=100, blank=True)  # e.g., "CBOT May 2024 + $50/MT"
    premium_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_value = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    
    # Delivery terms
    delivery_terms = models.CharField(max_length=3, choices=DELIVERY_TERMS, default='FOB')
    delivery_location = models.CharField(max_length=200, blank=True)
    loading_port = models.CharField(max_length=100, blank=True)
    discharge_port = models.CharField(max_length=100, blank=True)
    
    # Important dates
    contract_date = models.DateField(default=timezone.now)
    delivery_period_start = models.DateField()
    delivery_period_end = models.DateField()
    shipment_period_start = models.DateField(null=True, blank=True)
    shipment_period_end = models.DateField(null=True, blank=True)
    
    # Status and workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    approval_date = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_contracts')
    
    # Quality and specifications
    quality_specifications = models.TextField(blank=True)
    inspection_terms = models.TextField(blank=True)
    
    # Risk management
    hedge_required = models.BooleanField(default=False)
    hedge_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Additional terms
    payment_terms = models.CharField(max_length=100, blank=True)
    force_majeure_clause = models.TextField(blank=True)
    special_conditions = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Internal tracking
    internal_reference = models.CharField(max_length=50, blank=True)
    profit_center = models.CharField(max_length=50, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_contracts')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_contracts')

    class Meta:
        ordering = ['-contract_date', '-created_at']
        indexes = [
            models.Index(fields=['status', 'contract_date']),
            models.Index(fields=['counterparty', 'status']),
            models.Index(fields=['trader', 'contract_date']),
            models.Index(fields=['commodity', 'delivery_period_start']),
        ]

    def __str__(self):
        return f"{self.contract_number} - {self.counterparty} - {self.commodity}"

    def save(self, *args, **kwargs):
        if not self.contract_number:
            year = self.contract_date.year
            # Get the last contract number for the year
            last_contract = Contract.objects.filter(
                contract_number__startswith=f'CONT-{year}-'
            ).order_by('-contract_number').first()
            
            if last_contract:
                last_number = int(last_contract.contract_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.contract_number = f'CONT-{year}-{new_number:06d}'
        
        # Calculate total value
        if self.quantity and self.price:
            self.total_value = self.quantity * self.price
        
        super().save(*args, **kwargs)

    @property
    def days_to_delivery(self):
        if self.delivery_period_start:
            return (self.delivery_period_start - timezone.now().date()).days
        return None

    @property
    def is_overdue(self):
        if self.delivery_period_end and self.status not in ['completed', 'cancelled']:
            return timezone.now().date() > self.delivery_period_end
        return False

    @property
    def completion_percentage(self):
        # This would be calculated based on actual deliveries vs contracted quantity
        # For now, return 0 for all non-completed contracts
        if self.status == 'completed':
            return 100
        elif self.status == 'partially_executed':
            return 50  # This should be calculated from actual delivery records
        return 0


class ContractAmendment(models.Model):
    AMENDMENT_TYPES = [
        ('quantity', 'Quantity Change'),
        ('price', 'Price Change'),
        ('delivery_date', 'Delivery Date Change'),
        ('quality', 'Quality Specification Change'),
        ('other', 'Other'),
    ]

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='amendments')
    amendment_number = models.CharField(max_length=20)
    amendment_type = models.CharField(max_length=20, choices=AMENDMENT_TYPES)
    description = models.TextField()
    
    # Track what changed
    old_values = models.JSONField(default=dict)
    new_values = models.JSONField(default=dict)
    
    # Approval workflow
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='requested_amendments')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_amendments')
    approval_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['contract', 'amendment_number']

    def __str__(self):
        return f"{self.contract.contract_number} - Amendment {self.amendment_number}"