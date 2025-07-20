from django.urls import path
from .views import list_books, LibraryDetailView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail_view'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    

    path('admin_area/', views.admin_view, name='admin_area'),
    path('librarian_area/', views.librarian_view, name='librarian_area'),
    path('member_area/', views.member_view, name='member_area'),

    path('books/', views.book_list_all, name='book_list_all'), 
    path('books/add/', views.book_create, name='book_add'),
    path('books/<int:pk>/edit/', views.book_update, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),



]