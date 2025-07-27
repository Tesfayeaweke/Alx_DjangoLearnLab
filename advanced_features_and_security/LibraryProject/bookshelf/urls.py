# bookshelf/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views # Import Django's built-in auth views

from . import views # Import your views

app_name = 'bookshelf' # Define app_name for namespacing URLs (good practice)

urlpatterns = [
    # Book List View
    path('books/', views.BookListView.as_view(), name='book_list'),

    # Book Create View
    path('books/add/', views.BookCreateView.as_view(), name='book_create'),

    # Book Update View (requires a primary key 'pk')
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),

    # Book Delete View (requires a primary key 'pk')
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),

    # You might also want a detail view:
    # path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),

    # Dashboard Page (requires login)
    path('dashboard/', views.dashboard, name='dashboard'),

    # User Registration
    path('register/', views.register, name='register'),

    # Django's Built-in Login View
    # Use auth_views.LoginView.as_view() and specify the template
    path('login/', auth_views.LoginView.as_view(template_name='bookshelf/login.html'), name='login'),

    # Django's Built-in Logout View
    # Use auth_views.LogoutView.as_view() and specify the template (optional, often just redirects)
    path('logout/', auth_views.LogoutView.as_view(template_name='bookshelf/logout.html'), name='logout'),


    # --- Book Management Views (from previous step) ---
    # Book List View (e.g., /bookshelf/books/)
    path('books/', views.BookListView.as_view(), name='book_list'),

    # Book Create View (e.g., /bookshelf/books/add/)
    path('books/add/', views.BookCreateView.as_view(), name='book_create'),

    # Book Update View (e.g., /bookshelf/books/1/edit/)
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),

    # Book Delete View (e.g., /bookshelf/books/1/delete/)
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
]