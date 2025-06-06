#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Add the backend directory to Python path
sys.path.insert(0, '/mnt/c/Mis_Proyectos/Python/Next_CRM/Next_CRM/backend')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')

# Setup Django
django.setup()

print("=== CORS Settings ===")
print(f"CORS_ALLOW_ALL_ORIGINS: {getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', 'Not set')}")
print(f"CORS_ALLOWED_ORIGINS: {getattr(settings, 'CORS_ALLOWED_ORIGINS', 'Not set')}")
print(f"CORS_ALLOW_CREDENTIALS: {getattr(settings, 'CORS_ALLOW_CREDENTIALS', 'Not set')}")
print(f"INSTALLED_APPS has corsheaders: {'corsheaders' in settings.INSTALLED_APPS}")
print(f"MIDDLEWARE has CorsMiddleware: {'corsheaders.middleware.CorsMiddleware' in settings.MIDDLEWARE}")
print(f"Settings module: {settings.SETTINGS_MODULE}")