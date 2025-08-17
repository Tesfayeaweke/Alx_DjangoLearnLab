import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
    A custom filterset for the Book model, allowing filtering by
    'title', 'author', and 'publication_year'.
    """
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'author__name': ['exact', 'icontains'],
            'publication_year': ['exact', 'gte', 'lte'],
        }
