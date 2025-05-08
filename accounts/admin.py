from django.contrib import admin
from .models import ClientProfile, ArtisanProfile, AvailabilityOption, Service


# Register your models here.
admin.site.register(ClientProfile)
admin.site.register(ArtisanProfile)
admin.site.register(AvailabilityOption)
# admin.site.register(Service)