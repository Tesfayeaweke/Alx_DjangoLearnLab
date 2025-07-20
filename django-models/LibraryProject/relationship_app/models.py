from django.db import models

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
    
class library(models.Model):
    name  = models.CharField(100)
    books = models.ManyToManyField(Book)
    def __str__(self):
        return self.name
    
class Librarian(models.Model):
    name = models.CharField(100)
    Library = models.OneToOneField(Library,on_delete= models.CASCADE,related_name='librarian')
    def __str__(self):
        return self.name