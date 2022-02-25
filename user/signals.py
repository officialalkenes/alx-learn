from django.conf import settings
from django.dispatch import receiver

from django.db.models.signals import pre_save, post_save

from .models import Profile

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def auto_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

