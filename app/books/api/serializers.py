from books.models import Author, Book, Category
from django.utils.translation import gettext as _
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """Serializers for ingredients"""
    class Meta:
        model = Category
        fields = ['id', 'name',]
        read_only = ['id', 'slug']


class AuthorSerializer(serializers.ModelSerializer):
    """Serializers for Authors"""
    class Meta:
        model = Author
        fields = ['id', 'name', 'country']


class AuthorDetailSerializer(AuthorSerializer):
    """Serializers for author details"""
    class Meta(AuthorSerializer.Meta):
        fields = AuthorSerializer.Meta.fields + ['date_of_birth', 'country']


class BookSerializer(serializers.ModelSerializer):
    """Serializers for books"""
    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'category']


class BookDetailSerializer(BookSerializer):
    """Serializers for book details"""
    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + ['summary']
