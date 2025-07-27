# bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy # Used for reverse lookups in class-based views
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin # Important mixins
from django.views.generic import ListView, CreateView, UpdateView, DeleteView # Generic Views
from django.contrib import messages # For displaying messages to the user
from django.contrib.auth import get_user_model # If you need to reference CustomUser directly
from .models import Book # Import your Book model
from .forms import BookForm # Import your BookForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# --- Mixins for Permissions ---
# Instead of decorators, for Class-Based Views, it's best practice to use mixins.
# PermissionRequiredMixin is the class-based equivalent of @permission_required.

# View to list all books (requires 'can_view_book' permission)

CustomUser = get_user_model() # Assuming CustomUser is now in relationship_app/models.py
from relationship_app.models import UserProfile # Assuming UserProfile is in relationship_app/models.py

# --- General Site Navigation & Authentication Views ---

def home(request):
    """
    A simple home page view.
    """
    return render(request, 'bookshelf/home.html')

@login_required
def dashboard(request):
    """
    A simple dashboard view, requires user to be logged in.
    """
    return render(request, 'bookshelf/dashboard.html')

def register(request):
    """
    User registration view.
    """
    if request.method == 'POST':
        # Use Django's built-in UserCreationForm or your custom form if you made one
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('bookshelf:login') # Redirect to login page within bookshelf namespace
    else:
        form = UserCreationForm()
    return render(request, 'bookshelf/register.html', {'form': form})

class BookListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Book
    template_name = 'bookshelf/book_list.html' # Create this template
    context_object_name = 'books'
    permission_required = 'bookshelf.can_view_book' # The permission required to view this list
    login_url = '/login/' # Redirect to this URL if not logged in
    raise_exception = True # Raise 403 Forbidden if logged in but no permission

# View to create a new book (requires 'can_create_book' permission)
class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    form_class = BookForm # Use the form we defined
    template_name = 'bookshelf/book_form.html' # Create this template (can be reused for edit)
    success_url = reverse_lazy('bookshelf:book_list') # Redirect after successful creation
    permission_required = 'bookshelf.can_create_book'
    login_url = '/login/'
    raise_exception = True

    def form_valid(self, form):
        messages.success(self.request, 'Book created successfully!')
        return super().form_valid(form)

# View to edit an existing book (requires 'can_edit_book' permission)
class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'bookshelf/book_form.html' # Reuse the form template
    success_url = reverse_lazy('bookshelf:book_list')
    permission_required = 'bookshelf.can_edit_book'
    login_url = '/login/'
    raise_exception = True

    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully!')
        return super().form_valid(form)

# View to delete a book (requires 'can_delete_book' permission)
class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'bookshelf/book_confirm_delete.html' # Create this template
    success_url = reverse_lazy('bookshelf:book_list')
    permission_required = 'bookshelf.can_delete_book'
    login_url = '/login/'
    raise_exception = True

    def form_valid(self, form): # DeleteView's form_valid is called on POST to confirm delete
        messages.success(self.request, 'Book deleted successfully!')
        return super().form_valid(form)