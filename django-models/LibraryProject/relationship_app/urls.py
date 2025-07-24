# urls.py
from django.urls import path
from .views import list_books, LibraryDetailView
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register, name='register'),  # ← views.register (function-based)
    path('admin-role/', views.admin_view, name='admin_view'),
    path('librarian-role/', views.librarian_view, name='librarian_view'),
    path('member-role/', views.member_view, name='member_view'),
    
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),  # ← required pattern
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),  # ← required pattern
]
"""
views.register", "LogoutView.as_view(template_name=", "LoginView.as_view(template_name="

"""