from django.urls import path
from .views import (
    ListBooksView,
    RetrieveBookView,
    CreateBookView,
    UpdateBookView,
    DeleteBookView,
)

urlpatterns = [
    path('books/', ListBooksView.as_view(), name='book-list'),
    path('books/<int:pk>/', RetrieveBookView.as_view(), name='book-detail'),
    path('books/create/', CreateBookView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', UpdateBookView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', DeleteBookView.as_view(), name='book-delete'),
]
