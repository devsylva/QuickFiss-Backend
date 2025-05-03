from django.db import models
from django.contrib.auth import get_user_model
from core.models import Category, Tag
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
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    business_name = models.CharField(max_length=100)
    business_about = models.TextField()
    bio = models.TextField()
    language = models.CharField(max_length=100, choices=LANGUAGE)
    service_years = models.CharField(max_length=100)
    
    date_of_birth = models.DateField(blank=True, null=True)
    # country = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER)
    
    address = models.CharField(max_length=100)
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


