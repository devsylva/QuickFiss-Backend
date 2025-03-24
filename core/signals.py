from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from accounts.models import ClientProfile, ArtisanProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created and instance.is_client:
        ClientProfile.objects.create(user=instance)
    elif created and instance.is_artisan:
        ArtisanProfile.objects.create(user=instance)