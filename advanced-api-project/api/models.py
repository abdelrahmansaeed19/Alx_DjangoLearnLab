from django.db import models
from django.utils import timezone

"""
Models Summary:
---------------
- Author:
    Represents a book author with a name.
    One Author can have multiple Books.

- Book:
    Represents a single book with a title, publication year, and linked Author.
    Establishes a one-to-many relationship with Author using ForeignKey.
"""

# Author model: Represents an author who can have multiple books
class Author(models.Model):
    """Model representing an author with a name."""

    name = models.CharField(max_length=255)  # Author's full name

    def __str__(self) -> str:
        return self.name


# Book model: Represents a single book written by an author
class Book(models.Model):
    
    """
    Book model storing details of a single book.

    Fields:
    - title: Title of the book.
    - publication_year: Year the book was published (integer).
    - author: ForeignKey linking to Author, forming a one-to-many relationship.
    """
        
    title = models.CharField(max_length=255)  # Book title
    publication_year = models.IntegerField()  # Year book was published
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,  # Delete books if author is deleted
        related_name="books"       # Allows reverse access: author.books.all()
    )

    def __str__(self) -> str:
        return f"{self.title} ({self.publication_year})"
