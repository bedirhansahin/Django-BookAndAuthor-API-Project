from django.urls import path
from books.api import views

app_name = 'api_books'

urlpatterns = [
    path('books/list/', views.BookListView.as_view(), name='book-list'),
    
]
