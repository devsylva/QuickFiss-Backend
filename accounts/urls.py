from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


urlpatterns = [
    # auth
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('register/client/', views.ClientRegisterView.as_view(), name='client_register'),
    path('register/artisan/', views.ArtisanRegisterView.as_view(), name='artisan_register'),    
    path("otp/verify/", views.OTPVerificationView.as_view(), name="otp_verify"),

    # onboarding
    path('client/onboarding/', views.ClientOnboardingView.as_view(), name='client_onboarding'),
    path('artisan/onboarding/', views.ArtisanOnboardingView.as_view(), name='artiisan_onboarding'),
]