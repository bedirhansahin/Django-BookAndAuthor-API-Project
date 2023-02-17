from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from books.models import Category, Book, Author
from books.api.serializers import BookSerializer, BookDetailSerializer, AuthorSerializer, AuthorDetailSerializer


BOOK_URL = reverse('api_books:book-list')

def create_user(email='test@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email, password)

def detail_book_url(book_id):
    """Create and return a category url"""
    return reverse('api_books:book-detail', args=[book_id])

def create_book(user, **params):
    defaults = {
        'name': 'testbook',
        'summary': 'summarytestbook',
    }
    defaults.update(params)

    book = Book.objects.create(user=user, **defaults)
    return book

def create_author(user, **params):
    defaults = {
        'name': 'testauthor',
        'date_of_birth': '2023-01-01',
        'country': 'Turkey'
    }
    defaults.update(params)

    author = Author.objects.create(user=user, **defaults)
    return author

def create_category(user, **params):
    defaults = {
        'name': 'testcategory'
    }
    defaults.update(params)

    category = Category.objects.create(user=user, **defaults)
    return category


class PublicBookAPITests(TestCase):

    def setUp(self):
        """When a setUp() method is defined, the test runner will run that method prior to each test."""
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BOOK_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='test2@example.com',
            password='testpass1234',
            )
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass1234',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_books(self):
        create_book(user=self.user)
        create_book(user=self.user)

        res = self.client.get(BOOK_URL)

        books = Book.objects.all().order_by('id')
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_get_book_detail(self):
        book = create_book(user=self.user)
        url = detail_book_url(book.id)
        res = self.client.get(url)

        serializer = BookDetailSerializer(book)
        self.assertEqual(res.data, serializer.data)

    def test_full_update_book(self):
        book = create_book(
            user=self.user,
            name='testBook',
            summary = 'testSummary'
        )
        payload = {
            'name': 'newBookName',
            'summary': 'newSummary'
        }

        url = detail_book_url(book.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.user, self.user)

    def test_partial_update_book(self):
        summary = 'testSummary'
        book = create_book(
            user=self.user,
            name='testBook',
            summary = summary
        )
        payload = {
            'name': 'newBookName2'
        }

        url = detail_book_url(book.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.name, payload['name'])
        self.assertEqual(book.summary, summary)
        self.assertEqual(book.user, self.user)

    def test_delete_book(self):
        book = create_book(user=self.user)

        url = detail_book_url(book.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)