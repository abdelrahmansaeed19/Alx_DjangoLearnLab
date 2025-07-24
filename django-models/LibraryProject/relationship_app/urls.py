# urls.py
from django.urls import path
from .views import list_books, LibraryDetailView
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    add_book_view,
    edit_book_view,
    delete_book_view,
    book_list_view,
)

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register, name='register'),  # ← views.register (function-based)
    path('admin-role/', views.admin_view, name='admin_view'),
    path('librarian-role/', views.librarian_view, name='librarian_view'),
    path('member-role/', views.member_view, name='member_view'),
    path('books/add/', add_book_view, name='add_book'),
    path('books/edit/<int:pk>/', edit_book_view, name='edit_book'),
    path('books/delete/<int:pk>/', delete_book_view, name='delete_book'),
    
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),  # ← required pattern
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),  # ← required pattern
]
"""
views.register", "LogoutView.as_view(template_name=", "LoginView.as_view(template_name="

"""