import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Sample queries

# 1. Query all books by a specific author (e.g., author named "J.K. Rowling")
author_name = "J.K. Rowling"  # Replace with the actual author name
author = Author.objects.get(name=author_name)  # Replace 'author_name' with the actual author name
books_by_author = author.books.all()
objects = Book.objects.filter(author=author)  # Alternative way to get books by author
print(f"Books by {author.name}: {[book.title for book in books_by_author]}")

# 2. List all books in a library (e.g., library named "Central Library")
library_name = "Central Library"  # Replace with the actual library name
library = Library.objects.get(name=library_name)  # Replace 'library_name' with the actual library name
books_in_library = library.books.all()
print(f"Books in {library.name}: {[book.title for book in books_in_library]}")

# 3. Retrieve the librarian for a library (e.g., "Central Library")
librarian = Librarian.objects.get(library=library)
print(f"Librarian for {library.name}: {librarian.name}")
