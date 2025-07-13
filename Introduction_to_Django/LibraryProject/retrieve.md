>>> Book.objects.all()
<QuerySet [<Book: 1984>]>
>>> books = Book.objects.first()
>>> books.author
'George Orwell'
>>> books.title
'1984'
>>> books.publication_year
1949
