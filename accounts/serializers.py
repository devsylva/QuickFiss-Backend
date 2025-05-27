from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from core.models import Category, Service
from core.serializers import ServiceSerializer
from .models import ClientProfile, ArtisanProfile, AvailabilityOption
import re
from django.core.exceptions import ValidationError
import json

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']

    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Invalid email format")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


class AvailabilityOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilityOption
        fields = ["name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ClientProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    preferred_categories = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    preferred_categories_data = CategorySerializer(
        source='preferred_categories',
        many=True,
        read_only=True
    )
    profile_picture = serializers.ImageField(required=False)
    date_of_birth = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = ClientProfile
        fields = [
            'first_name', 'last_name', 
            'profile_picture', 'date_of_birth', 
            'preferred_categories', 'preferred_categories_data'
            ]

    def validate_preferred_categories(self, value):
        if isinstance(value, list) and len(value) == 1 and isinstance(value[0], str):
            try:
                # Attempt to parse as JSON if it looks like a stringified list
                parsed_value = json.loads(value[0])
                if isinstance(parsed_value, list):
                    value = parsed_value
            except json.JSONDecodeError:
                pass  # Not a JSON string, proceed with original value

        # Ensure value is a list of strings
        if not isinstance(value, list):
            raise serializers.ValidationError("preferred_categories must be a list of category names")

        # Get valid category names from Category.CATEGORY choices
        valid_categories = [choice[0] for choice in Category.CATEGORY]
        
        for category_name in value:
            if not isinstance(category_name, str):
                raise serializers.ValidationError(f"Category name must be a string: {category_name}")
            if category_name not in valid_categories:
                raise serializers.ValidationError(
                    f"Invalid category: '{category_name}'. Valid options are: {valid_categories}"
                )
        return value

    def update(self, instance, validated_data):
        # Handle preferred_categories list
        preferred_categories_data = validated_data.pop('preferred_categories', None)
        
        # Update scalar fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.save()

        # Update preferred_categories if provided
        if preferred_categories_data is not None:
            # Clear existing categories
            instance.preferred_categories.clear()
            # Add new categories by name
            for category_name in preferred_categories_data:
                category, _ = Category.objects.get_or_create(name=category_name)
                instance.preferred_categories.add(category)

        return instance


class ArtisanKYCSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=["Male", "Female"], required=False)
    address = serializers.CharField(required=False)
    proof_of_address = serializers.FileField(required=False)
    landmark = serializers.CharField(required=False)

    class Meta:
        model = ArtisanProfile
        fields = [
            'first_name', 'last_name', 
            'profile_picture', 'date_of_birth', 
            'gender', 'address', 'proof_of_address', 'landmark'
        ]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)    
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.address = validated_data.get('address', instance.address)
        instance.proof_of_address = validated_data.get('proof_of_address', instance.proof_of_address)
        instance.landmark = validated_data.get('landmark', instance.landmark)
        instance.save()

        return instance


class ArtisanCutomizationSerializer(serializers.ModelSerializer):
    services = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    service_data = ServiceSerializer(
        source='services',
        many=True,
        read_only=True
    )
    availability = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    availability_data = AvailabilityOptionSerializer(
        source='availability',
        many=True,
        read_only=True
    )
    business_name = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    experience = serializers.CharField(required=False)
    certification = serializers.FileField(required=False)
    language = serializers.ChoiceField(choices=["English", "Pidgin", "French", "Yoruba", "Hausa", "Igbo", "Others"], required=False)
    business_about = serializers.CharField(required=False)
    experience = serializers.ChoiceField(choices=[
        "1", "2", "3", "4", "5"
        "6", "7", "8", "9", "10"
    ],required=False)
    location = serializers.CharField(required=False)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = ArtisanProfile
        fields = [
            'business_name', 'bio', 
            'experience', 'language', 
            'availability', 'availability_data', 'location', 'experience',
            'business_about', 'services', 'service_data',
            'min_price', 'max_price', 'certification',
        ]  

    def validate_services(self, value):
        if isinstance(value, list) and len(value) == 1 and isinstance(value[0], str):
            try:
                parsed_value = json.loads(value[0])
                if isinstance(parsed_value, list):
                    value = parsed_value
            except json.JSONDecodeError:
                pass

        if not isinstance(value, list):
            raise serializers.ValidationError("service must be a list of service names")

        if value:
            valid_service_names = set(Service.objects.values_list('name', flat=True))
            invalid_services = [name for name in value if name not in valid_service_names]
            if invalid_services:
                raise serializers.ValidationError(
                    f"The following service names are invalid: {', '.join(invalid_services)}"
                )

        return value

    def validate_availability(self, value):
        if isinstance(value, list) and len(value) == 1 and isinstance(value[0], str):
            try:
                parsed_value = json.loads(value[0])
                if isinstance(parsed_value, list):
                    value = parsed_value
            except json.JSONDecodeError:
                pass

        if not isinstance(value, list):
            raise serializers.ValidationError("availability must be a list of availability names")

        if value:
            valid_availability_options = set(AvailabilityOption.objects.values_list('name', flat=True))
            invalid_availability = [name for name in value if name not in valid_availability_options]
            if invalid_availability:
                raise serializers.ValidationError(
                    f"The following availability options are invalid: {', '.join(invalid_availability)}"
                )

        return value

    def update(self, instance, validated_data):
        services_data = validated_data.pop('services', None)
        availability_option_data = validated_data.pop('availability', None)
        
        instance.business_name = validated_data.get('business_name', instance.first_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.certification = validated_data.get('certification', instance.certification)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.business_about = validated_data.get('business_about', instance.business_about)
        instance.language = validated_data.get('language', instance.language)
        instance.location = validated_data.get('location', instance.location)
        instance.min_price = validated_data.get('min_price', instance.min_price)
        instance.max_price = validated_data.get('max_price', instance.max_price)
        instance.save()

        if services_data is not None:
            instance.service.clear()
            for service_name in services_data:
                service, _ = Service.objects.get_or_create(name=service_name)
                instance.service.add(service)

        if availability_option_data is not None:
            instance.availability.clear()
            for availability_name in availability_option_data:
                availability_option, _ = AvailabilityOption.objects.get_or_create(name=availability_name)
                instance.availability.add(availability_option)

        return instance


