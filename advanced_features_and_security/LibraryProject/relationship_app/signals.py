from django.db.models.signals import post_save # Signal sent after a model's save() method is called
from django.dispatch import receiver # Decorator to register a function as a signal receiver
from django.contrib.auth.models import User # Django's built-in User model
from .models import UserProfile # Your custom UserProfile model
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@receiver(post_save, sender=User) # Decorator: This function will be called after a User object is saved
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # If a new User was just created, create a corresponding UserProfile
        UserProfile.objects.create(user=instance)