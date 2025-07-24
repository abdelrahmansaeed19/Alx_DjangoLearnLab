# views.py
from django.http import HttpResponse
from django.shortcuts import render
from .models import Book, Library
from django.views.generic import DetailView

def book_list_view(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'