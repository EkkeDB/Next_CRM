from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('gdpr/consent/', views.GDPRConsentView.as_view(), name='gdpr_consent'),
    path('gdpr/export/', views.UserDataExportView.as_view(), name='user_data_export'),
    path('account/delete/', views.delete_account, name='delete_account'),
]