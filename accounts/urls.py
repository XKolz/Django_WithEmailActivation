# accounts/urls.py
from django.urls import path
from .views import RegisterView, LoginView, PasswordResetRequestView, PasswordResetConfirmView, ProfileView, ActivateAccountView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
        path('register/', RegisterView.as_view(), name='register'),
        path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
        path('login/', LoginView.as_view(), name='login'), # Custom login view
        path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
        path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
        path('profile/', ProfileView.as_view(), name='profile'),
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # JWT login endpoint
]
