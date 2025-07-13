>>> books = Book.objects.get(id=1)
>>> books.delete()
(0, {'bookshelf.Book': 0})
