# bookshelf/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year'] # Adjust fields as per your Book model

class ExampleForm(forms.Form):
    """
    A simple example form to demonstrate input handling and validation.
    """
    # A text field for user input
    text_input = forms.CharField(
        label='Enter some text',
        max_length=200,
        help_text='This field will be validated for safe input.'
    )
    # An optional integer field
    number_input = forms.IntegerField(
        label='Enter a number (optional)',
        required=False,
        min_value=0,
        max_value=1000
    )

    # You can add custom clean methods for more complex validation
    def clean_text_input(self):
        data = self.cleaned_data['text_input']
        # Example of custom validation: ensure no specific forbidden words
        if "badword" in data.lower():
            raise forms.ValidationError("This word is not allowed!")
        return data
