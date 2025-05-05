from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import  APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, ClientProfileSerializer, ArtisanKYCSerializer
from .models import OTPVerification, ClientProfile, ArtisanProfile
from .tasks import send_otp_email
from .permissions import IsArtisan, IsClient

User = get_user_model()

# Create your views here.

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


class UserRegistrationView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        serializer = ClientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # generate OTP
            otp = OTPVerification.objects.create(user=user).generate_otp()
            # send OTP verification Email Asynchronously
            send_otp_email.delay(user.email, otp)

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User created successfully, Kindly check your email for OTP verification",
                "user": {"id": user.id, "email": user.email},
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            if user.is_active:  
                return Response({"error": "Email is already verified"}, status=status.HTTP_400_BAD_REQUEST)

            # Check for existing OTP record and update it, or create a new one
            otp_record, created = OTPVerification.objects.get_or_create(user=user)
            otp = otp_record.generate_otp()  # Generate new OTP and update the record

            # Send OTP email asynchronously
            send_otp_email.delay(user.email, otp)

            return Response({
                "message": "OTP resent successfully, please check your email"
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)


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


# Client Onboarding Vies
class ClientOnboardingView(APIView):
    permission_classes = [IsClient,]

    def put(self, request):
        try:
            profile = ClientProfile.objects.get(user=request.user)
            serializer = ClientProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ClientProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)


class ArtisanKYCView(APIView):
    permission_classes = [IsArtisan,]

    def put(self, request):
        try:
            profile = ArtisanProfile.objects.get(user=request.user)
            serializer = ArtisanKYCSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ArtisanProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)


class ArtisanCustomizationView(APIView):
    permission_classes = [IsArtisan,]

    pass