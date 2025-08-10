"""
Tests for the advanced_api_project Book API.

This file contains unit tests for:
- CRUD operations (create, retrieve, update, delete)
- Permissions enforcement (authenticated vs unauthenticated)
- Filtering, searching and ordering behavior

How tests work:
- Uses Django's test runner which creates a separate test database automatically.
- Uses rest_framework.test.APIClient and APITestCase.
- Authentication is simulated with `force_authenticate` to avoid having to implement token flows here.
- Endpoints referenced by name via `reverse()` (expects your urls.py to include the names:
  'book-list', 'book-detail', 'book-create', 'book-update', 'book-delete').

Run:
    python manage.py test api
"""

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Author, Book

User = get_user_model()


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user (authenticated actions)
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Create authors
        self.author_rowling = Author.objects.create(name="J. K. Rowling")
        self.author_orwell = Author.objects.create(name="George Orwell")

        # Create some books
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author_rowling
        )
        self.book2 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author_orwell
        )
        self.client = APIClient()  # instance used for requests

        # Reverse-resolved endpoints (expects names present in `api/urls.py`)
        self.list_url = reverse('book-list')              # /api/books/
        self.create_url = reverse('book-create')          # /api/books/create/
        self.detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})  # /api/books/<pk>/
        self.update_url = lambda pk: reverse('book-update', kwargs={'pk': pk})  # /api/books/update/<pk>/
        self.delete_url = lambda pk: reverse('book-delete', kwargs={'pk': pk})  # /api/books/delete/<pk>/

    # ---------------------------
    # Read-only endpoints (public)
    # ---------------------------
    def test_list_books_public(self):
        """GET /books/ should be allowed for anonymous users and return list of books."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expect at least the two created books
        titles = [item['title'] for item in response.json()]
        self.assertIn(self.book1.title, titles)
        self.assertIn(self.book2.title, titles)

    def test_retrieve_book_public(self):
        """GET /books/<pk>/ should be allowed for anonymous users and return book data."""
        response = self.client.get(self.detail_url(self.book1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['title'], self.book1.title)
        self.assertEqual(data['publication_year'], self.book1.publication_year)

    # ---------------------------
    # Create / Update / Delete (auth required)
    # ---------------------------
    def test_create_book_requires_auth(self):
        """Unauthenticated POST to create should be rejected (401/403)."""
        payload = {"title": "New Book", "publication_year": 2020, "author": self.author_rowling.pk}
        response = self.client.post(self.create_url, payload, format='json')
        # Accept either 401 Unauthorized or 403 Forbidden depending on auth config
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated(self):
        """Authenticated POST creates a book and returns 201 and the created data."""
        self.client.force_authenticate(user=self.user)
        payload = {"title": "New Book", "publication_year": 2020, "author": self.author_rowling.pk}
        response = self.client.post(self.create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        # self.assertEqual(data['title'], payload['title'])
        self.assertEqual(response.data['title'], payload['title'])
        
        # Confirm it exists in DB
        self.assertTrue(Book.objects.filter(title=payload['title']).exists())

    def test_update_book_requires_auth(self):
        """Unauthenticated PUT should be rejected."""
        payload = {"title": "Changed Title", "publication_year": 1997, "author": self.author_rowling.pk}
        response = self.client.put(self.update_url(self.book1.pk), payload, format='json')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_update_book_authenticated(self):
        """Authenticated PUT updates the book."""
        self.client.force_authenticate(user=self.user)
        payload = {"title": "Changed Title", "publication_year": 1997, "author": self.author_rowling.pk}
        response = self.client.put(self.update_url(self.book1.pk), payload, format='json')
        # UpdateAPIView often returns 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Changed Title")

    def test_delete_book_requires_auth(self):
        """Unauthenticated DELETE should be rejected."""
        response = self.client.delete(self.delete_url(self.book2.pk))
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_delete_book_authenticated(self):
        """Authenticated DELETE removes the book from the DB."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.delete_url(self.book2.pk))
        self.assertIn(response.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    # ------------------------------------
    # Filtering, Searching and Ordering
    # ------------------------------------
    def test_filter_by_publication_year(self):
        """Filtering by publication_year should return only matching books."""
        # Filter for 1997
        response = self.client.get(f"{self.list_url}?publication_year=1997")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(all(item['publication_year'] == 1997 for item in data))
        self.assertTrue(any(item['title'] == self.book1.title for item in data))

    def test_search_by_title(self):
        """Search (query parameter `search`) should match by title or author."""
        response = self.client.get(f"{self.list_url}?search=1984")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item['title'] for item in response.json()]
        self.assertIn(self.book2.title, titles)

    def test_ordering_by_publication_year(self):
        """Ordering should return results sorted by publication_year ascending."""
        response = self.client.get(f"{self.list_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [item['publication_year'] for item in response.json()]
        self.assertEqual(years, sorted(years))

    # ---------------------------
    # Permission checks summary
    # ---------------------------
    def test_read_is_public_write_requires_auth(self):
        """Quick summary test: list is public but create requires auth."""
        # public list
        self.client.force_authenticate(user=None)
        r = self.client.get(self.list_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        # write should fail anonymous
        payload = {"title": "Another", "publication_year": 2000, "author": self.author_rowling.pk}
        r2 = self.client.post(self.create_url, payload, format='json')
        self.assertIn(r2.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
