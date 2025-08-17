from django.db import models
class Author(models.Model):
    """
    The Author model stores information about a book's author.
    It has a one-to-many relationship with the Book model, meaning one
    author can be associated with multiple books. This relationship is
    established through the ForeignKey on the Book model.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    The Book model stores information about a book.
    It is linked to the Author model via a ForeignKey, which establishes
    the one-to-many relationship (one Author can have many Books).
    The 'related_name' attribute 'books' allows us to access all books
    from an author instance, for example, author.books.all().
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name='books',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
