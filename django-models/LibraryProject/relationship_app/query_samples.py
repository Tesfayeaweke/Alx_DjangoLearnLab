from relationship_app.models import Author,Book,Library,Librarian

# Query all books by a specific author.
authors = Author.objects.all()
for author in authors:
     for book in author.book.all():
             print(book.title)

# List all books in a library.
library = Library.objects.all()
for item in library:
    for book in item.books.all():
        print(book.title)

# Retrieve the librarian for a library.
librarian = Librarian.objects.all()
for library in librarian:
     print(library.name)