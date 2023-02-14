from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from books.models import Category


CATEGORY_URL = reverse('api_books:category-list')
BOOK_URL = reverse('api_books:book-list')
AUTHOR_URL = reverse('api_books:author-list')

def create_user(email='test@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email, password)

def detail_category_url(category_id):
    """Create and return a category url"""
    return reverse('api_books:category-detail', args=[category_id])


class PublicAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        """When a setUp() method is defined, the test runner will run that method prior to each test."""
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(CATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)




class PrivateCategoryAPIViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)


    def test_category_list_success(self):
        payload = {
            'name': 'test category'
        }
        res = self.client.get(CATEGORY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_category_create_success(self):
        payload = {
            'name': 'test category'
        }
        res = self.client.post(CATEGORY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
