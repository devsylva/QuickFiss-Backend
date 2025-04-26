from django.db import models
from core.models import User
import random

# Create your models here.
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.user.get_full_name()}".strip()


class ArtisanProfile(models.Model):
    GENDER = (
        ("M", "Male"),
        ("F", "Femaile"),
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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    business_about = models.TextField()
    bio = models.TextField()
    language = models.CharField(max_length=100, choices=LANGUAGE)
    service_years = models.CharField(max_length=100)
    
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER)
    
    address = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    about = models.TextField()

    # images
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    certification = models.FileField(upload_to='certifications/', blank=True, null=True)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.user.get_full_name()}".strip()


class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)


    def generate_otp(self):
        self.otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.save()
        return self.otp