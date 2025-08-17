from django.urls import path
from .views import BookListCreateView, BookDetailView, BookUpdateView, BookDeleteView

urlpatterns = [
    # Endpoint for listing all books and creating a new one.
    # Maps to /api/books/
    path('books/', BookListCreateView.as_view(), name='book-list-create'),

    # Endpoint for retrieving a single book by its ID.
    # Maps to /api/books/<pk>/
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Endpoint for updating an existing book.
    # Maps to /api/books/<pk>/update/
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    
    # Endpoint for deleting an existing book.
    # Maps to /api/books/<pk>/delete/
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
