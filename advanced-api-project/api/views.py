from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter

class BookListView(generics.ListAPIView):
    """
    API view for retrieving a list of all books, with advanced query capabilities.

    - A GET request retrieves a list of all Book objects.
    - Filtering, searching, and ordering are now supported via query parameters.
    - Example usage:
        - Filtering by publication year: /api/books/?publication_year=1949
        - Searching by title or author: /api/books/?search=animal
        - Ordering by title (descending): /api/books/?ordering=-title
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Configure the filter backends to be used for this view.
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Specify the filterset class from the new filters.py file.
    filterset_class = BookFilter

    # Define the fields that can be searched.
    search_fields = ['title', 'author__name']

    # Define the fields that can be used for ordering.
    ordering_fields = ['title', 'publication_year']


class BookDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving a single book by its primary key (pk).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    API view for creating a new book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    API view for updating a single book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        book_id = self.request.data.get('id')
        if not book_id:
            return Response({'error': 'ID must be provided in the request body for this endpoint.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            return self.get_queryset().get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': f'Book with id {book_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Response as e:
            return e
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class BookDeleteView(generics.DestroyAPIView):
    """
    API view for deleting a single book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        book_id = self.request.data.get('id')
        if not book_id:
            return Response({'error': 'ID must be provided in the request body for this endpoint.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            return self.get_queryset().get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': f'Book with id {book_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Response as e:
            return e

