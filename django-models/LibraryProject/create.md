>>> from Bookshelf.models import Book
from library.models import Book
Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
# Expected output: <Book: 1984>
<QuerySet [<Book: Book object (1)>]>
