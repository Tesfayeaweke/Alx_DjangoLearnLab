from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Library,Book,Author,Librarian
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User # Import User model if you need to access it directly
from .models import UserProfile # Import your UserProfile model to use its role constants


def list_books(request):
    books = Book.objects.all()
    context = {'book_list': books}

    return render(request,'relationship_app/list_books.html', context)



# Create your views here.
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()  # Access related books
        return context

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created successfully for {user.username}! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})

def is_admin(user):
    """Checks if the user is authenticated and has an 'Admin' role."""
    # Ensure user is authenticated and has a profile linked
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == UserProfile.ADMIN

def is_librarian(user):
    """
    Checks if the user is authenticated and has a 'Librarian' role.
    Admins are also considered Librarians for access purposes.
    """
    return user.is_authenticated and hasattr(user, 'profile') and \
           (user.profile.role == UserProfile.LIBRARIAN or user.profile.role == UserProfile.ADMIN)

def is_member(user):
    """
    Checks if the user is authenticated and has any valid role ('Member', 'Librarian', or 'Admin').
    Essentially, any logged-in user with a profile.
    """
    return user.is_authenticated and hasattr(user, 'profile') and \
           (user.profile.role == UserProfile.MEMBER or \
            user.profile.role == UserProfile.LIBRARIAN or \
            user.profile.role == UserProfile.ADMIN)

@login_required # This decorator ensures only logged-in users can access this view
def dashboard(request):
    """
    A simple dashboard view for logged-in users.
    Displays the user's username.
    """
    return render(request, 'relationship_app/dashboard.html', {'user': request.user})

def home(request):
    """
    The main landing page of the application.
    Displays different content based on whether the user is authenticated.
    """
    return render(request, 'relationship_app/home.html')

# --- Role-Based Access Views ---

@login_required # User must be logged in to access
@user_passes_test(is_admin, login_url='/login/') # User must pass the 'is_admin' check
def admin_view(request):
    """
    View accessible only to users with the 'Admin' role.
    """
    return render(request, 'relationship_app/admin_view.html', {'user': request.user, 'role': request.user.profile.role})

@login_required # User must be logged in to access
@user_passes_test(is_librarian, login_url='/login/') # User must pass the 'is_librarian' check
def librarian_view(request):
    """
    View accessible only to users with the 'Librarian' or 'Admin' role.
    """
    return render(request, 'relationship_app/librarian_view.html', {'user': request.user, 'role': request.user.profile.role})

@login_required # User must be logged in to access
@user_passes_test(is_member, login_url='/login/') # User must pass the 'is_member' check
def member_view(request):
    """
    View accessible to all authenticated users ('Member', 'Librarian', 'Admin').
    """
    return render(request, 'relationship_app/member_view.html', {'user': request.user, 'role': request.user.profile.role})

