from rest_framework import serializers
from .models import Author, Book
from django.utils import timezone

class BookSerializer(serializers.ModelSerializer):
    """
    The BookSerializer handles the serialization of the Book model.
    It serializes all fields of the Book model.
    """
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate_publication_year(self, value):
        """
        Custom validator to ensure the publication year is not in the future.
        If the year is in the future, it raises a validation error.
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    The AuthorSerializer handles the serialization of the Author model.
    It includes a nested BookSerializer to show all books written by an
    author directly in the author's representation. This is done by
    using the 'related_name' ('books') defined in the Book model's
    ForeignKey field.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

