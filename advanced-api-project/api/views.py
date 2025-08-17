from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    """
    API view for listing all books and creating a new book.

    - A GET request retrieves a list of all Book objects.
      This is permitted for all users, including unauthenticated users.
    - A POST request creates a new Book object.
      This is restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Define permissions for this view. Read-only for all, write for authenticated.
    def get_permissions(self):
        if self.request.method == 'POST':
            # Use IsAuthenticated permission for creation (POST)
            return [permissions.IsAuthenticated()]
        # Use IsAuthenticatedOrReadOnly for read-only methods (GET)
        return [permissions.IsAuthenticatedOrReadOnly()]

class BookDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving a single book by its primary key (pk).

    - A GET request retrieves a specific Book object.
      This is permitted for all users, including unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookUpdateView(generics.UpdateAPIView):
    """
    API view for updating a single book.

    - A PUT/PATCH request updates a specific Book object.
      This is restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    """
    API view for deleting a single book.

    - a DELETE request removes a specific Book object.
      This is restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]