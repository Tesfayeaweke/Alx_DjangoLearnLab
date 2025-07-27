# relationship_app/forms.py
from django import forms
from .models import Author, Book, Library, Librarian 

class BookForm(forms.ModelForm):
    # You can customize fields here if needed, e.g., widgets, help_texts
    class Meta:
        model = Book
        fields = ['title', 'author']
