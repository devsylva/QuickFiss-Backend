from django.contrib import admin
from .models import ClientProfile, ArtisanProfile


# Register your models here.
admin.site.register(ClientProfile)
admin.site.register(ArtisanProfile)