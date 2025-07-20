from relationship_app.models import Author,Book,Library,Librarian

# Query all books by a specific author.
author = Author.objects.get(name=author_name)
for book in author.book.all():
     print(book.title)

# List all books in a library.
library = Library.objects.get(name=library_name)
for book in library.books.all():
     print(book.title)

# Retrieve the librarian for a library.
librarian = Librarian.objects.all()
for library in librarian:
     print(library.name)