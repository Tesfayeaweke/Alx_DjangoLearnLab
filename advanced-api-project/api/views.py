rom rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    """
    API view for retrieving a list of all books.

    - A GET request retrieves a list of all Book objects.
      This is permitted for all users, including unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving a single book by its primary key (pk).

    - A GET request retrieves a specific Book object.
      This is permitted for all users, including unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    """
    API view for creating a new book.

    - A POST request creates a new Book object.
      This is restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    """
    API view for updating a single book.

    This view is configured to get the book ID from the request body,
    as no ID is provided in the URL.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Override the default behavior to get the ID from the request body.
        book_id = self.request.data.get('id')
        if not book_id:
            raise ValueError('ID must be provided in the request body for this endpoint.')
        
        try:
            return self.get_queryset().get(id=book_id)
        except Book.DoesNotExist:
            raise ValueError(f'Book with id {book_id} not found.')
            
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class BookDeleteView(generics.DestroyAPIView):
    """
    API view for deleting a single book.

    This view is configured to get the book ID from the request body,
    as no ID is provided in the URL.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Override the default behavior to get the ID from the request body.
        book_id = self.request.data.get('id')
        if not book_id:
            raise ValueError('ID must be provided in the request body for this endpoint.')
        
        try:
            return self.get_queryset().get(id=book_id)
        except Book.DoesNotExist:
            raise ValueError(f'Book with id {book_id} not found.')

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
