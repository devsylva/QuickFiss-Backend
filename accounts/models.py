from django.db import models
from core.models import User
import random

# Create your models here.
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class ArtisanProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    about = models.TextField()

    def __str__(self):
        return self.full_name


class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)


    def generate_otp(self):
        self.otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.save()
        return self.otp