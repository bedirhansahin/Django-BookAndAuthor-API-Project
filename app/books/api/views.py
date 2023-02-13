from django.contrib.auth import get_user_model
from rest_framework import authentication, generics, permissions
from rest_framework.authtoken import views
from rest_framework.settings import api_settings

from books.api.serializers import BookListSerializer
from books.models import Book

