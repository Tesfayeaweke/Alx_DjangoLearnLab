from django.shortcuts import render
from django.views.generic import DetailView
from .models import Author,Book,Library,Librarian
def book_list(request):
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

