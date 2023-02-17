from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from books.models import Category
from books.api.serializers import CategorySerializer


CATEGORY_URL = reverse('api_books:category-list')

def create_user(email='test@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email, password)

def detail_category_url(category_id):
    """Create and return a category url"""
    return reverse('api_books:category-detail', args=[category_id])

def create_category(user, **params):
    defaults = {
        'name': 'testcategory'
    }
    defaults.update(params)

    category = Category.objects.create(user=user, **defaults)
    return category


class PublicCategoryAPITests(TestCase):

    def setUp(self):
        """When a setUp() method is defined, the test runner will run that method prior to each test."""
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(CATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryAPITests(TestCase):
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

    def test_retrieve_category(self):
        create_category(user=self.user)
        create_category(user=self.user)

        res = self.client.get(CATEGORY_URL)

        categories = Category.objects.all().order_by('id')
        serializer = CategorySerializer(categories, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_update_category(self):
        category = create_category(
            user=self.user,
            name = 'Test Category'
        )
        payload = {
            'name': 'Test Category Update'
        }

        url = detail_category_url(category.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.user, self.user)

    def test_delete_category(self):
        category = create_category(user=self.user)

        url = detail_category_url(category.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)