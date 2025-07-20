from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    name  = models.CharField(100)
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(100)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='book')
    def __str__(self):
        return self.title
    
class Library(models.Model):
    name  = models.CharField(100)
    books = models.ManyToManyField(Book)
    def __str__(self):
        return self.name
    
class Librarian(models.Model):
    name = models.CharField(100)
    library = models.OneToOneField(Library,on_delete= models.CASCADE,related_name='librarian')
    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    # Define role choices as constants for clarity and reusability
    ADMIN = 'Admin'
    LIBRARIAN = 'Librarian'
    MEMBER = 'Member'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (LIBRARIAN, 'Librarian'),
        (MEMBER, 'Member'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=MEMBER)
    def __str__(self):
        return f"{self.user.username}'s Profile ({self.role})"

