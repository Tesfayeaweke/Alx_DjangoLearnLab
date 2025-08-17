from rest_framework import serializers
from .models import Author, Book
from django.utils import timezone

class BookSerializer(serializers.ModelSerializer):
    """
    The BookSerializer handles the serialization of the Book model.
    It serializes all fields of the Book model and includes a custom
    validation method to ensure data integrity.
    """
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        """
        Custom validator to ensure the publication year is not in the future.
        If the year is in the future, it raises a validation error.
        This is an example of custom data validation within a serializer.
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    The AuthorSerializer handles the serialization of the Author model.
    It demonstrates a nested relationship by including a list of related books.
    The relationship between Author and Book is handled by defining the 'books'
    field. This field uses the BookSerializer with 'many=True' to serialize
    the related books dynamically. The name 'books' matches the 'related_name'
    defined on the ForeignKey in the Book model, which allows DRF to automatically
    fetch the related objects.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
