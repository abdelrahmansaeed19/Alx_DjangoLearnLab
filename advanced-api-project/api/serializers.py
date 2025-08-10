from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book

"""
Serializers Summary:
--------------------
- BookSerializer:
    Serializes all Book fields.
    Includes validation to ensure publication_year is not in the future.

- AuthorSerializer:
    Serializes the Author's name and includes a nested BookSerializer for related books.
    Uses the 'related_name' from Book model (author.books.all()) to fetch books.
"""


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Serializes all fields and validates that publication_year is not in the future.
    """

    class Meta:
        model = Book
        fields = "__all__"

    def validate_publication_year(self, value):
        """Ensure publication_year is not greater than the current year."""
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future (current year: {current_year})."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Serializes 'name' and includes nested books via BookSerializer.
    """
    books = BookSerializer(many=True, read_only=True)  # Uses related_name='books'

    class Meta:
        model = Author
        fields = ["name", "books"]
