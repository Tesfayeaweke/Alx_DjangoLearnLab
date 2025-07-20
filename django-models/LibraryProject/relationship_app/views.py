from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Library,Book,Author,Librarian
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login

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

