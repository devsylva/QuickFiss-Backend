from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from core.models import Category
from .models import ClientProfile, ArtisanProfile
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
    pass