# bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy # Used for reverse lookups in class-based views
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin # Important mixins for CBVs
from django.views.generic import ListView, CreateView, UpdateView, DeleteView # Generic Class-Based Views
from django.contrib import messages # For displaying messages to the user
from django.contrib.auth import get_user_model # To dynamically get the active user model
from django.contrib.auth.decorators import login_required # For function-based views like dashboard/home
from django.contrib.auth.forms import UserCreationForm # For register view

from .models import Book # Import your Book model
from .forms import BookForm # Import your BookForm

# Get the CustomUser model, which is defined in relationship_app/models.py
# This ensures we're always referencing the correct user model.
CustomUser = get_user_model()
# Assuming UserProfile is defined in relationship_app/models.py
from relationship_app.models import UserProfile


# --- General Site Navigation & Authentication Views ---
# These views handle basic site navigation and user authentication flows.

def home(request):
    """
    Renders the home page of the application.
    This view does not require authentication or specific permissions.
    """
    return render(request, 'bookshelf/home.html')

@login_required # Decorator: Ensures user is logged in to access this view
def dashboard(request):
    """
    Renders the user dashboard.
    Only authenticated users can access this view.
    """
    return render(request, 'bookshelf/dashboard.html')

def register(request):
    """
    Handles user registration.
    User input for registration is handled by Django's forms (UserCreationForm),
    which perform built-in validation and ensure password hashing for security.
    This prevents common vulnerabilities like SQL injection and insecure password storage.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # Uses Django's built-in UserCreationForm
        if form.is_valid():
            form.save() # Django's form.save() uses the ORM, preventing SQL injection.
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('bookshelf:login') # Redirects to the login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'bookshelf/register.html', {'form': form})


# --- Book Management Views with Permission Enforcement and Secure Data Access ---
# All these Class-Based Views (CBVs) manage CRUD operations for the Book model.
# They use Django's ModelForms and ORM for data interaction, which inherently
# protects against SQL Injection. User input is validated by the forms before
# being saved to the database.

class BookListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Displays a list of all books.
    Requires: User must be logged in.
              User must have 'bookshelf.can_view_book' permission.
    Data retrieval via `model = Book` (Django ORM) is secure against SQL injection.
    """
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.can_view_book' # The specific permission required
    login_url = reverse_lazy('bookshelf:login') # Updated: Redirect to bookshelf:login if not logged in
    raise_exception = True # Raise 403 Forbidden if logged in but no permission

class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Handles the creation of new book entries.
    Requires: User must be logged in.
              User must have 'bookshelf.can_create_book' permission.
    Uses `form_class = BookForm` (a ModelForm) for input validation and
    secure saving via the ORM, preventing SQL injection.
    """
    model = Book
    form_class = BookForm # Uses the custom BookForm for input
    template_name = 'bookshelf/book_form.html'
    success_url = reverse_lazy('bookshelf:book_list') # Redirects to book list after creation
    permission_required = 'bookshelf.can_create_book'
    login_url = reverse_lazy('bookshelf:login') # Updated: Redirect to bookshelf:login if not logged in
    raise_exception = True

    def form_valid(self, form):
        # form.save() uses Django's ORM, which parameterizes queries, preventing SQL injection.
        messages.success(self.request, 'Book created successfully!') # User feedback message
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Handles the updating of existing book entries.
    Requires: User must be logged in.
              User must have 'bookshelf.can_edit_book' permission.
    Uses `form_class = BookForm` (a ModelForm) for input validation and
    secure saving via the ORM, preventing SQL injection.
    """
    model = Book
    form_class = BookForm
    template_name = 'bookshelf/book_form.html'
    success_url = reverse_lazy('bookshelf:book_list') # Redirects to book list after update
    permission_required = 'bookshelf.can_edit_book'
    login_url = reverse_lazy('bookshelf:login') # Updated: Redirect to bookshelf:login if not logged in
    raise_exception = True

    def form_valid(self, form):
        # form.save() uses Django's ORM, which parameterizes queries, preventing SQL injection.
        messages.success(self.request, 'Book updated successfully!') # User feedback message
        return super().form_valid(form)

class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Handles the deletion of book entries.
    Requires: User must be logged in.
              User must have 'bookshelf.can_delete_book' permission.
    Deletion via `model = Book` and Django's ORM is secure.
    """
    model = Book
    template_name = 'bookshelf/book_confirm_delete.html'
    success_url = reverse_lazy('bookshelf:book_list') # Redirects to book list after deletion
    permission_required = 'bookshelf.can_delete_book'
    login_url = reverse_lazy('bookshelf:login') # Updated: Redirect to bookshelf:login if not logged in
    raise_exception = True

    def form_valid(self, form): # DeleteView's form_valid is called on POST to confirm delete
        messages.success(self.request, 'Book deleted successfully!') # User feedback message
        return super().form_valid(form)
