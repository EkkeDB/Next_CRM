from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, GDPRRecord, AuditLog, LoginAttempt


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    readonly_fields = ('created_at', 'updated_at', 'gdpr_consent_date', 'last_login_ip')


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')


@admin.register(GDPRRecord)
class GDPRRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'consent_type', 'consent_given', 'consent_date', 'ip_address')
    list_filter = ('consent_type', 'consent_given', 'consent_date')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('consent_date', 'ip_address', 'user_agent')
    ordering = ('-consent_date',)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'object_repr', 'timestamp', 'ip_address')
    list_filter = ('action', 'model_name', 'timestamp')
    search_fields = ('user__username', 'object_repr', 'ip_address')
    readonly_fields = ('id', 'timestamp', 'ip_address', 'user_agent', 'session_key')
    ordering = ('-timestamp',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('username', 'ip_address', 'successful', 'timestamp', 'failure_reason')
    list_filter = ('successful', 'timestamp')
    search_fields = ('username', 'ip_address')
    readonly_fields = ('timestamp', 'user_agent')
    ordering = ('-timestamp',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)