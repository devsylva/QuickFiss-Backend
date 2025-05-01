from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import ClientProfile, ArtisanProfile
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    # Handle creation
    if created:
        if instance.is_client:
            ClientProfile.objects.create(user=instance)
        elif instance.is_artisan:
            ArtisanProfile.objects.create(user=instance)
    # Handle updates
    else:
        if instance.is_client:
            # Ensure ClientProfile exists, create if it doesn't
            ClientProfile.objects.get_or_create(user=instance)
            #delete ArtisanProfile if it exists
            ArtisanProfile.objects.filter(user=instance).delete()
        elif instance.is_artisan:
            # Ensure ArtisanProfile exists, create if it doesn't
            ArtisanProfile.objects.get_or_create(user=instance)
            #delete ClientProfile if it exists
            ClientProfile.objects.filter(user=instance).delete()
        else:
            # If neither client nor artisan, delete both profiles
            ClientProfile.objects.filter(user=instance).delete()
            ArtisanProfile.objects.filter(user=instance).delete()