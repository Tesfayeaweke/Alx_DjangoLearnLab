>>> books = Book.objects.get(id=1)
>>> books.title = 'Nineteen Eighty-Four'
>>> books.save()
>>> books.title
'Nineteen Eighty-Four'