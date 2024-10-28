# accounts/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.core.mail import EmailMultiAlternatives
from rest_framework import serializers
from django.utils.http import urlsafe_base64_encode


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  # User is inactive until email is confirmed
        )

        # Send confirmation email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = f"{settings.SITE_URL}{reverse('accounts:activate', kwargs={'uidb64': uid, 'token': token})}"
        
        message = render_to_string('accounts/activation_email.html', {
            'user': user,
            'activation_link': activation_link,
        })

        # Use EmailMultiAlternatives to send HTML email
        email = EmailMultiAlternatives(
            subject="Activate your account",
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(message, "text/html")  # Attach the HTML content
        email.send()

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        
        # Ensure the user is active
        if not user.is_active:
            raise serializers.ValidationError("User account is inactive")

        data['user'] = user
        return data

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user is associated with this email address.")
        return value

    def save(self):
        user = self.user
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        reset_link = f"{settings.SITE_URL}{reverse('accounts:password-reset-confirm', kwargs={'uidb64': uid, 'token': token})}"
        
        message = render_to_string('accounts/password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        
        # Use EmailMultiAlternatives to send HTML email
        email = EmailMultiAlternatives(
            subject="Activate your account",
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(message, "text/html")  # Attach the HTML content
        email.send()
  
class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        uidb64 = self.context.get('uidb64')
        token = self.context.get('token')
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid token or user ID.")

        if not account_activation_token.check_token(user, token):
            raise serializers.ValidationError("Token is invalid or has expired.")

        data['user'] = user
        return data

    def save(self):
        # Get user and new password from validated data
        user = self.validated_data['user']
        password = self.validated_data['new_password']
        
        # Set the new password and save the user
        user.set_password(password)
        user.save()
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        