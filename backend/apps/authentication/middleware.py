from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class JWTCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_auth = JWTAuthentication()
        
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        
        if access_token:
            try:
                validated_token = jwt_auth.get_validated_token(access_token)
                user = jwt_auth.get_user(validated_token)
                request.user = user
                request.auth = validated_token
            except (InvalidToken, TokenError) as e:
                logger.debug(f"Invalid JWT token: {e}")
                request.user = AnonymousUser()
                request.auth = None
        else:
            request.user = AnonymousUser()
            request.auth = None

        response = self.get_response(request)
        return response


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        if not settings.DEBUG:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if hasattr(request, '_audit_log_data'):
            from .models import AuditLog
            from .utils import get_client_ip
            
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=request._audit_log_data.get('action'),
                model_name=request._audit_log_data.get('model_name'),
                object_id=request._audit_log_data.get('object_id'),
                object_repr=request._audit_log_data.get('object_repr'),
                changes=request._audit_log_data.get('changes', {}),
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                session_key=request.session.session_key,
            )
        
        return response