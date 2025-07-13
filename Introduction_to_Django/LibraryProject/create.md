>>> from Bookshelf.models import Book
>>> post_1 = Book(title = '1984', author = 'George Orwell', publication_year = 1949)
>>> post_1.save()
>>> Book.objects.all()
<QuerySet [<Book: Book object (1)>]>
