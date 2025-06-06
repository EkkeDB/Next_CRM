from django.urls import path
from . import views

urlpatterns = [
    # URLs without trailing slashes (to avoid CORS-breaking redirects)
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('token/refresh', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('password/change', views.PasswordChangeView.as_view(), name='password_change'),
    path('gdpr/consent', views.GDPRConsentView.as_view(), name='gdpr_consent'),
    path('gdpr/export', views.UserDataExportView.as_view(), name='user_data_export'),
    path('account/delete', views.delete_account, name='delete_account'),
    path('test-cors', views.test_cors, name='test_cors'),
    path('debug-cors', views.debug_cors_simple, name='debug_cors_simple'),
    
    # Keep trailing slash versions for backward compatibility
    path('register/', views.RegisterView.as_view(), name='register_slash'),
    path('login/', views.LoginView.as_view(), name='login_slash'),
    path('logout/', views.LogoutView.as_view(), name='logout_slash'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh_slash'),
    path('profile/', views.ProfileView.as_view(), name='profile_slash'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change_slash'),
    path('gdpr/consent/', views.GDPRConsentView.as_view(), name='gdpr_consent_slash'),
    path('gdpr/export/', views.UserDataExportView.as_view(), name='user_data_export_slash'),
    path('account/delete/', views.delete_account, name='delete_account_slash'),
    path('test-cors/', views.test_cors, name='test_cors_slash'),
    path('debug-cors/', views.debug_cors_simple, name='debug_cors_simple_slash'),
]