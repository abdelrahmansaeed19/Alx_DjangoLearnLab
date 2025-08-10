from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

"""
Views Summary:
--------------
- ListBooksView: List all books (read-only, public access)
- RetrieveBookView: Retrieve a single book by ID (read-only, public access)
- CreateBookView: Create a new book (authenticated users only)
- UpdateBookView: Update an existing book (authenticated users only)
- DeleteBookView: Delete a book (authenticated users only)

We use DRF's generic class-based views for efficient CRUD handling.
Permissions are applied to restrict modifications to authenticated users.
"""


class ListBooksView(generics.ListAPIView):
    """Retrieve a list of all books."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access


class RetrieveBookView(generics.RetrieveAPIView):
    """Retrieve a single book by its ID."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access


class CreateBookView(generics.CreateAPIView):
    """Create a new book. Only for authenticated users."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     """
    #     Hook to customize creation behavior if needed.
    #     For now, just saves the validated book instance.
    #     """
    #     serializer.save()

    def perform_create(self, serializer):
        if not serializer.validated_data.get("publication_year"):
            serializer.save(publication_year=timezone.now().year)
        else:
            serializer.save()



class UpdateBookView(generics.UpdateAPIView):
    """Update an existing book. Only for authenticated users."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Hook to customize update behavior if needed.
        Currently just saves updated data.
        """
        serializer.save()


class DeleteBookView(generics.DestroyAPIView):
    """Delete a book. Only for authenticated users."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


