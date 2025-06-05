from django.conf import settings
from django.contrib.auth.models import User
from .models import LoginAttempt, AuditLog
import logging

logger = logging.getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_login_attempt(request, username, successful, failure_reason=''):
    LoginAttempt.objects.create(
        username=username,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        successful=successful,
        failure_reason=failure_reason
    )


def log_audit_event(request, action, model_name='', object_id=None, object_repr='', changes=None):
    request._audit_log_data = {
        'action': action,
        'model_name': model_name,
        'object_id': object_id,
        'object_repr': object_repr,
        'changes': changes or {}
    }


def set_jwt_cookies(response, access_token, refresh_token):
    response.set_cookie(
        settings.SIMPLE_JWT['AUTH_COOKIE'],
        access_token,
        max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
        path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
    )
    
    response.set_cookie(
        settings.SIMPLE_JWT['REFRESH_COOKIE'],
        refresh_token,
        max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        httponly=settings.SIMPLE_JWT['REFRESH_COOKIE_HTTP_ONLY'],
        secure=settings.SIMPLE_JWT['REFRESH_COOKIE_SECURE'],
        samesite=settings.SIMPLE_JWT['REFRESH_COOKIE_SAMESITE'],
        domain=settings.SIMPLE_JWT['REFRESH_COOKIE_DOMAIN'],
        path=settings.SIMPLE_JWT['REFRESH_COOKIE_PATH'],
    )


def clear_jwt_cookies(response):
    response.delete_cookie(
        settings.SIMPLE_JWT['AUTH_COOKIE'],
        domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
        path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
    )
    
    response.delete_cookie(
        settings.SIMPLE_JWT['REFRESH_COOKIE'],
        domain=settings.SIMPLE_JWT['REFRESH_COOKIE_DOMAIN'],
        path=settings.SIMPLE_JWT['REFRESH_COOKIE_PATH'],
    )


def create_user_profile(user, **profile_data):
    from .models import UserProfile
    
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults=profile_data
    )
    
    if not created:
        for key, value in profile_data.items():
            setattr(profile, key, value)
        profile.save()
    
    return profile