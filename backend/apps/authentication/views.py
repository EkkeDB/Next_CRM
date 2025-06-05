from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from .models import UserProfile, GDPRRecord, AuditLog
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    PasswordChangeSerializer, GDPRConsentSerializer
)
from .utils import (
    get_client_ip, log_login_attempt, log_audit_event,
    set_jwt_cookies, clear_jwt_cookies
)


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
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['REFRESH_COOKIE'])
        
        if not refresh_token:
            return Response({
                'error': 'Refresh token not found'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        request.data['refresh'] = refresh_token
        
        try:
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
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
            response = Response({
                'error': 'Invalid refresh token'
            }, status=status.HTTP_401_UNAUTHORIZED)
            clear_jwt_cookies(response)
            return response


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

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