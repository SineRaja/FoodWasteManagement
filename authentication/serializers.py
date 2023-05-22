from django.contrib.auth import get_user_model
from rest_framework import serializers
from .validations import validate_email


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password', 'gender', 'user_type')


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email',)
        extra_kwargs = {
            'email': {
                'validators': [validate_email]
            }
        }


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
        extra_kwargs = {
            'email': {
                'validators': [validate_email]
            }
        }


class PasswordResetSerializer(EmailSerializer):
    pass


class PasswordResetVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=40)


class PasswordResetVerifiedSerializer(PasswordResetVerifySerializer):
    password = serializers.CharField(max_length=128)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'id', 'phone_number', 'gender', 'user_type')


class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'phone_number', 'gender')


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'id', 'phone_number', 'gender')
