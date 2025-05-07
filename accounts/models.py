from django.db import models
from django.contrib.auth import get_user_model
from core.models import Category, Tag, Service
import random

User = get_user_model()

# Create your models here.
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    preferred_categories = models.ManyToManyField(Category, blank=True)
    followed_tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.user.email


class ArtisanProfile(models.Model):
    GENDER = (
        ("M", "Male"),
        ("F", "Female"),
    )

    LANGUAGE = (
        ("English", "English"),
        ("Pidgin", "Pidgin"),
        ("French", "French"),
        ("Yoruba", "Yoruba"),
        ("Hausa", "Hausa"),
        ("Igbo", "Igbo"),
        ("Others", "Others"),
    )

    # AVAILABILITY_CHOICES = (
    #     ("MORNING", "Morning"),
    #     ("AFTERNOON", "Afternoon"),
    #     ("NIGHT", "Night"),
    # )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    business_name = models.CharField(max_length=100)
    business_about = models.TextField()
    bio = models.TextField()
    language = models.CharField(max_length=100, choices=LANGUAGE)
    service = models.ManyToManyField(Service, blank=True)
    service_years = models.CharField(max_length=100)

    # Price range fields (min and max for slider)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    
    date_of_birth = models.DateField(blank=True, null=True)
    availability = models.ManyToManyField("AvailabilityOption")
    gender = models.CharField(max_length=10, choices=GENDER)
    
    location = models.CharField(max_length=100, blank=True)
    landmark = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    about = models.TextField()

    # files
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    certification = models.FileField(upload_to='certifications/', blank=True, null=True)
    proof_of_address = models.FileField(upload_to='proof_of_address/', blank=True, null=True)

    def __str__(self):
        return self.user.email


class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)


    def generate_otp(self):
        self.otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        self.save()
        return self.otp


class AvailabilityOption(models.Model):
    name = models.CharField(
        max_length=10,
        choices=[
            ('MORNING', 'Morning'),
            ('AFTERNOON', 'Afternoon'),
            ('NIGHT', 'Night'),
        ]
    )
    def __str__(self):
        return self.get_name_display()