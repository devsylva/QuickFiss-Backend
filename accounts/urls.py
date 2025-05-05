from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


urlpatterns = [
    # auth
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('resend-otp/', views.ResendOTPView.as_view(), name='otp_resend'),
    path("verify-otp/", views.OTPVerificationView.as_view(), name="otp_verify"),

    # onboarding
    path('client/onboarding/', views.ClientOnboardingView.as_view(), name='client_onboarding'),
    path('artisan/kyc/', views.ArtisanKYCView.as_view(), name='artiisan_onboarding'),
]