from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from .models import UserProfile, GDPRRecord, AuditLog
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    PasswordChangeSerializer, GDPRConsentSerializer
)
from .utils import (
    get_client_ip, log_login_attempt, log_audit_event,
    set_jwt_cookies, clear_jwt_cookies
)
import time


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        log_audit_event(request, 'CREATE', 'User', user.id, str(user))
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            
            # Reset failed attempts on successful login
            if hasattr(user, 'profile'):
                user.profile.reset_failed_attempts()
                user.profile.last_login_ip = get_client_ip(request)
                user.profile.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # Create response with tokens in cookies
            response = Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            }, status=status.HTTP_200_OK)
            
            set_jwt_cookies(response, str(access_token), str(refresh))
            
            log_login_attempt(request, user.username, True)
            log_audit_event(request, 'LOGIN', 'User', user.id, str(user))
            
            return response
            
        except Exception as e:
            username = request.data.get('username', '')
            
            # Increment failed attempts for existing user
            try:
                user = User.objects.get(username=username)
                if hasattr(user, 'profile'):
                    user.profile.increment_failed_attempts()
            except User.DoesNotExist:
                pass
            
            log_login_attempt(request, username, False, str(e))
            
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['REFRESH_COOKIE'])
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            response = Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
            
            clear_jwt_cookies(response)
            
            log_audit_event(request, 'LOGOUT', 'User', request.user.id, str(request.user))
            
            return response
            
        except Exception as e:
            response = Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
            clear_jwt_cookies(response)
            return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        client_ip = get_client_ip(request)
        cache_key = f"refresh_circuit_breaker:{client_ip}"
        
        # Check circuit breaker
        failure_count = cache.get(cache_key, 0)
        if failure_count >= 5:  # After 5 failures, block for 5 minutes
            cache.set(cache_key, failure_count, 300)  # 5 minutes
            return Response({
                'error': 'Too many failed refresh attempts. Please login again.',
                'code': 'CIRCUIT_BREAKER_OPEN'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['REFRESH_COOKIE'])
        
        if not refresh_token:
            # Increment failure count
            cache.set(cache_key, failure_count + 1, 300)
            response = Response({
                'error': 'Refresh token not found',
                'code': 'NO_REFRESH_TOKEN'
            }, status=status.HTTP_401_UNAUTHORIZED)
            clear_jwt_cookies(response)
            return response
        
        request.data['refresh'] = refresh_token
        
        try:
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
                # Reset circuit breaker on success
                cache.delete(cache_key)
                
                access_token = response.data['access']
                
                # Create new response with token in cookie
                new_response = Response({
                    'message': 'Token refreshed successfully'
                }, status=status.HTTP_200_OK)
                
                new_response.set_cookie(
                    settings.SIMPLE_JWT['AUTH_COOKIE'],
                    access_token,
                    max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )
                
                return new_response
            
            return response
            
        except (TokenError, InvalidToken):
            # Increment failure count
            cache.set(cache_key, failure_count + 1, 300)
            
            response = Response({
                'error': 'Invalid refresh token',
                'code': 'INVALID_REFRESH_TOKEN'
            }, status=status.HTTP_401_UNAUTHORIZED)
            clear_jwt_cookies(response)
            return response


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        log_audit_event(request, 'UPDATE', 'UserProfile', 
                       self.get_object().id, str(self.get_object()))
        return response


class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        log_audit_event(request, 'UPDATE', 'User', request.user.id, 'Password changed')
        
        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)


class GDPRConsentView(generics.ListCreateAPIView):
    serializer_class = GDPRConsentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GDPRRecord.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        log_audit_event(request, 'CREATE', 'GDPRRecord', 
                       response.data.get('id'), 'GDPR consent updated')
        return response


class UserDataExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)
        
        user_data = {
            'personal_info': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
            },
            'profile': {
                'phone': profile.phone if profile else '',
                'company': profile.company if profile else '',
                'position': profile.position if profile else '',
                'timezone': profile.timezone if profile else '',
                'gdpr_consent': profile.gdpr_consent if profile else False,
                'gdpr_consent_date': profile.gdpr_consent_date if profile else None,
            },
            'gdpr_records': list(
                GDPRRecord.objects.filter(user=user).values(
                    'consent_type', 'consent_given', 'consent_date'
                )
            ),
            'audit_logs': list(
                AuditLog.objects.filter(user=user).values(
                    'action', 'model_name', 'timestamp'
                )[:100]  # Last 100 entries
            )
        }
        
        log_audit_event(request, 'EXPORT', 'User', user.id, 'Data export requested')
        
        return Response(user_data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_account(request):
    user = request.user
    
    # Anonymize user data instead of hard delete for audit trail
    user.username = f"deleted_user_{user.id}"
    user.email = f"deleted_{user.id}@example.com"
    user.first_name = "Deleted"
    user.last_name = "User"
    user.is_active = False
    user.save()
    
    if hasattr(user, 'profile'):
        profile = user.profile
        profile.phone = ""
        profile.company = ""
        profile.position = ""
        profile.gdpr_consent = False
        profile.save()
    
    log_audit_event(request, 'DELETE', 'User', user.id, 'Account deletion requested')
    
    response = Response({
        'message': 'Account deleted successfully'
    }, status=status.HTTP_200_OK)
    
    clear_jwt_cookies(response)
    
    return response


@api_view(['GET', 'POST', 'OPTIONS'])
@permission_classes([permissions.AllowAny])
def test_cors(request):
    """Comprehensive CORS test endpoint with detailed debugging"""
    import json
    from django.conf import settings
    
    # Collect detailed request information
    request_info = {
        'method': request.method,
        'path': request.path,
        'full_path': request.get_full_path(),
        'scheme': request.scheme,
        'is_secure': request.is_secure(),
        'headers': {},
        'cookies': dict(request.COOKIES),
        'user_authenticated': request.user.is_authenticated,
        'user': str(request.user) if request.user.is_authenticated else 'Anonymous',
    }
    
    # Collect all headers
    for key, value in request.META.items():
        if key.startswith('HTTP_'):
            header_name = key[5:].replace('_', '-').title()
            request_info['headers'][header_name] = value
    
    # Add some non-HTTP headers that are important
    for key in ['CONTENT_TYPE', 'CONTENT_LENGTH', 'REQUEST_METHOD', 'QUERY_STRING']:
        if key in request.META:
            request_info['headers'][key] = request.META[key]
    
    # CORS configuration info
    cors_info = {
        'CORS_ALLOWED_ORIGINS': getattr(settings, 'CORS_ALLOWED_ORIGINS', []),
        'CORS_ALLOW_ALL_ORIGINS': getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', False),
        'CORS_ALLOW_CREDENTIALS': getattr(settings, 'CORS_ALLOW_CREDENTIALS', False),
        'CORS_ALLOW_HEADERS': getattr(settings, 'CORS_ALLOW_HEADERS', []),
        'CORS_ALLOW_METHODS': getattr(settings, 'CORS_ALLOW_METHODS', []),
    }
    
    # Environment info
    env_info = {
        'DEBUG': settings.DEBUG,
        'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
        'DJANGO_SETTINGS_MODULE': request.META.get('DJANGO_SETTINGS_MODULE', 'Not set'),
    }
    
    # Create response data
    response_data = {
        'status': 'success',
        'message': 'CORS debug test endpoint',
        'timestamp': timezone.now().isoformat(),
        'request_info': request_info,
        'cors_config': cors_info,
        'environment': env_info,
        'debugging_tips': [
            'Check browser network tab for actual headers sent/received',
            'Look at the Origin header - it should match your frontend URL',
            'Verify Access-Control-Allow-Origin header in response',
            'For credentials: ensure CORS_ALLOW_CREDENTIALS=True and specific origins',
            'Check for preflight OPTIONS requests before actual requests',
        ]
    }
    
    response = JsonResponse(response_data, json_dumps_params={'indent': 2})
    
    # Force CORS headers for debugging (should be redundant with middleware)
    origin = request.META.get('HTTP_ORIGIN')
    if origin:
        response['Access-Control-Allow-Origin'] = origin
    else:
        response['Access-Control-Allow-Origin'] = '*'
    
    response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRFToken'
    response['Access-Control-Allow-Credentials'] = 'true'
    response['Access-Control-Max-Age'] = '86400'
    
    return response


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def debug_cors_simple(request):
    """Simple CORS test without authentication"""
    return JsonResponse({
        'message': 'Simple CORS test - no auth required',
        'origin': request.META.get('HTTP_ORIGIN', 'No origin'),
        'method': request.method,
        'timestamp': timezone.now().isoformat(),
    })