from books.api import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('authors', views.AuthorViewSet)
router.register('books', views.BookViewSet)

app_name = 'api_books'

urlpatterns = [
    path('', include(router.urls)),
]
