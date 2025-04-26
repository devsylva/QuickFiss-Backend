from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import  APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ClientRegisterSerializer, ArtisanRegisterSerializer
from .models import OTPVerification, User
from .tasks import send_otp_email
from .permissions import IsArtisan, IsClient

# Create your views here.
#
class LogOutView(APIView):
    permission_class = [IsAuthenticated,]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ClientRegisterView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        serializer = ClientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # generate OTP
            otp = OTPVerification.objects.create(user=user).generate_otp()
            # send OTP verification Email Asynchronously
            send_otp_email(user.email, otp)

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User created successfully, Kindly check your email for OTP verification",
                "user": {"id": user.id, "email": user.email},
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArtisanRegisterView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        serializer = ArtisanRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # generate OTP
            otp = OTPVerification.objects.create(user=user).generate_otp()
            # send OTP verification Email Asynchronously
            send_otp_email(user.email, otp)

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User created successfully, Kindly check your email for OTP verification",
                "user": {"id": user.id, "email": user.email},
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerificationView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        try:
            otp = request.data['otp']
            user_id = request.data['user_id']
            user = User.objects.get(id=user_id)
            otp_verification = OTPVerification.objects.get(user=user)
            if otp_verification.otp == otp:
                otp_verification.is_verified = True
                otp_verification.save()
                user.is_active = True
                user.save()
                return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
            return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


# Artisan's Onboarding Views
class ArtisanOnboardingView(APIView):
    permission_classes = [IsArtisan]

    