>>> book = Book.objects.get(id=1)
>>> book.delete()
(0, {'bookshelf.Book': 0})
