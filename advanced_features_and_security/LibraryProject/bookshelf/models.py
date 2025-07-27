from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return self.title

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, username, password=None, **extra_fields):
        
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email) # Normalize the email address

        # Create the user instance
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password) # Hash the password
        user.save(using=self._db) # Save to the database

        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) # Superusers should always be active

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Call the create_user method to handle basic user creation
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser):
    
    date_of_birth = models.DateField(
        null=True, # Allows the field to be NULL in the database
        blank=True # Allows the field to be blank in forms
    )
    profile_photo = models.ImageField(
        upload_to='profile_pics/', # Directory where uploaded images will be stored
        null=True, # Allows the field to be NULL in the database
        blank=True # Allows the field to be blank in forms
    )

    # Assign the custom manager to your CustomUser model
    objects = CustomUserManager()


    def __str__(self):
        return self.username
