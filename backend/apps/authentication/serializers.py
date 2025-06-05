from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import UserProfile, GDPRRecord
from .utils import get_client_ip


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    company = serializers.CharField(max_length=100, required=False, allow_blank=True)
    position = serializers.CharField(max_length=100, required=False, allow_blank=True)
    gdpr_consent = serializers.BooleanField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 
                 'password_confirm', 'phone', 'company', 'position', 'gdpr_consent')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        
        if not attrs.get('gdpr_consent', False):
            raise serializers.ValidationError("GDPR consent is required.")
        
        return attrs

    def create(self, validated_data):
        password_confirm = validated_data.pop('password_confirm')
        phone = validated_data.pop('phone', '')
        company = validated_data.pop('company', '')
        position = validated_data.pop('position', '')
        gdpr_consent = validated_data.pop('gdpr_consent')
        
        user = User.objects.create_user(**validated_data)
        
        request = self.context.get('request')
        ip_address = get_client_ip(request) if request else None
        
        UserProfile.objects.create(
            user=user,
            phone=phone,
            company=company,
            position=position,
            gdpr_consent=gdpr_consent,
            gdpr_consent_date=user.date_joined,
            gdpr_consent_ip=ip_address
        )
        
        if gdpr_consent:
            GDPRRecord.objects.create(
                user=user,
                consent_type='data_processing',
                consent_given=True,
                ip_address=ip_address,
                user_agent=request.META.get('HTTP_USER_AGENT', '') if request else ''
            )
        
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError("Invalid credentials.")
            
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            
            # Check if account is locked
            if hasattr(user, 'profile') and user.profile.is_account_locked():
                raise serializers.ValidationError("Account is temporarily locked due to failed login attempts.")
            
            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError("Must include username and password.")


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    last_login = serializers.DateTimeField(source='user.last_login', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'company', 
                 'position', 'timezone', 'date_joined', 'last_login', 'gdpr_consent',
                 'gdpr_consent_date', 'is_mfa_enabled')
        read_only_fields = ('gdpr_consent_date', 'is_mfa_enabled')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class GDPRConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GDPRRecord
        fields = ('consent_type', 'consent_given', 'consent_date')
        read_only_fields = ('consent_date',)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        validated_data['ip_address'] = get_client_ip(request)
        validated_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
        return super().create(validated_data)