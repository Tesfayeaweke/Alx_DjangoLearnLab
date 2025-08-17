from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITests(APITestCase):
    """
    Test suite for the Book model API endpoints.
    """
    
    def setUp(self):
        """
        Set up the test data and authenticated user for all tests.
        """
        # Create test authors
        self.author1 = Author.objects.create(name='Jane Austen')
        self.author2 = Author.objects.create(name='George Orwell')

        # Create test books
        self.book1 = Book.objects.create(
            title='Pride and Prejudice', 
            publication_year=1813, 
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984', 
            publication_year=1949, 
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='Animal Farm', 
            publication_year=1945, 
            author=self.author2
        )
        
        # Create an authenticated user for testing restricted endpoints
        self.user = User.objects.create_user(username='testuser', password='password123')
        
    # --- Test CRUD Operations ---
    
    def test_book_list_view(self):
        """
        Test retrieving a list of all books from the list view endpoint.
        """
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the response data contains all three books
        self.assertEqual(len(response.data), 3)

    def test_book_detail_view(self):
        """
        Test retrieving a single book from the detail view endpoint.
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the returned data matches the book's title
        self.assertEqual(response.data['title'], 'Pride and Prejudice')
    
    def test_book_create_authenticated(self):
        """
        Test creating a new book as an authenticated user.
        Should return HTTP 201 Created.
        """
        url = reverse('book-create')
        # Simulate user login for the request
        self.client.login(username='testuser', password='password123')
        data = {
            'title': 'The Hitchhiker\'s Guide to the Galaxy',
            'publication_year': 1979,
            'author': self.author2.id  # Use the author's ID
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify that the book was added to the database
        self.assertEqual(Book.objects.count(), 4)
        
    def test_book_create_unauthenticated(self):
        """
        Test creating a new book as an unauthenticated user.
        Should be rejected with HTTP 401 Unauthorized.
        """
        url = reverse('book-create')
        data = {
            'title': 'The Hitchhiker\'s Guide to the Galaxy',
            'publication_year': 1979,
            'author': self.author2.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Verify that no book was added to the database
        self.assertEqual(Book.objects.count(), 3)
        
    def test_book_update_authenticated(self):
        """
        Test updating an existing book as an authenticated user.
        Should return HTTP 200 OK.
        """
        url = reverse('book-update')
        # Simulate user login for the request
        self.client.login(username='testuser', password='password123')
        data = {
            'id': self.book1.id,
            'title': 'New Title',
            'publication_year': 2000
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the book's title was actually updated in the database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'New Title')
        
    def test_book_update_unauthenticated(self):
        """
        Test updating a book as an unauthenticated user.
        Should be rejected with HTTP 401 Unauthorized.
        """
        url = reverse('book-update')
        data = {
            'id': self.book1.id,
            'title': 'New Title',
            'publication_year': 2000
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Verify the book was not updated
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.title, 'New Title')
        
    def test_book_delete_authenticated(self):
        """
        Test deleting a book as an authenticated user.
        Should return HTTP 204 No Content.
        """
        url = reverse('book-delete')
        # Simulate user login for the request
        self.client.login(username='testuser', password='password123')
        data = {'id': self.book1.id}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify the book was deleted from the database
        self.assertEqual(Book.objects.count(), 2)

    def test_book_delete_unauthenticated(self):
        """
        Test deleting a book as an unauthenticated user.
        Should be rejected with HTTP 401 Unauthorized.
        """
        url = reverse('book-delete')
        data = {'id': self.book1.id}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Verify the book was not deleted
        self.assertEqual(Book.objects.count(), 3)
    
    # --- Test Filtering, Searching, and Ordering ---
    
    def test_book_list_filter_by_publication_year(self):
        """
        Test filtering the book list by publication year.
        """
        url = reverse('book-list') + '?publication_year=1949'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')
        
    def test_book_list_search_by_title(self):
        """
        Test searching for a book by its title.
        """
        url = reverse('book-list') + '?search=pride'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Pride and Prejudice')
        
    def test_book_list_search_by_author_name(self):
        """
        Test searching for books by the author's name.
        """
        url = reverse('book-list') + '?search=George'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_book_list_ordering_by_title(self):
        """
        Test ordering the book list by title in ascending order.
        """
        url = reverse('book-list') + '?ordering=title'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify the order: Animal Farm, 1984, Pride and Prejudice
        self.assertEqual(response.data[0]['title'], '1984')
        self.assertEqual(response.data[1]['title'], 'Animal Farm')
        self.assertEqual(response.data[2]['title'], 'Pride and Prejudice')
        
    def test_book_list_ordering_by_publication_year_descending(self):
        """
        Test ordering the book list by publication year in descending order.
        """
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify the order: 1984, Animal Farm, Pride and Prejudice
        self.assertEqual(response.data[0]['publication_year'], 1949)
        self.assertEqual(response.data[1]['publication_year'], 1945)
        self.assertEqual(response.data[2]['publication_year'], 1813)
