from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from .models import User, UserProfile
from django.contrib.auth import get_user_model
from django.conf import settings
import os

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if os.environ.get("CREATE_SUPERUSER", "False") == "True":
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
            password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
            User.objects.create_superuser(email=email, password=password)
            print(f"Superuser {email} created successfully")
