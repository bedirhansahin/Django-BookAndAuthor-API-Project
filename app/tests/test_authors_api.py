from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from books.models import Author
from books.api.serializers import AuthorSerializer, AuthorDetailSerializer


AUTHOR_URL = reverse('api_books:author-list')

def create_user(email='test@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email, password)

def detail_author_url(author_id):
    """Create and return a category url"""
    return reverse('api_books:author-detail', args=[author_id])

def create_author(user, **params):
    defaults = {
        'name': 'testauthor',
        'date_of_birth': '2023-01-01',
        'country': 'Turkey',
        'biography': 'Some Biography staff'
    }
    defaults.update(params)

    author = Author.objects.create(user=user, **defaults)
    return author


class PublicAuthorAPITests(TestCase):

    def setUp(self):
        """When a setUp() method is defined, the test runner will run that method prior to each test."""
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AUTHOR_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAuthorAPITests(TestCase):

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

    def test_retrieve_authors(self):
        create_author(user=self.user)
        create_author(user=self.user)

        res = self.client.get(AUTHOR_URL)

        authors = Author.objects.all().order_by('id')
        serializer = AuthorSerializer(authors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_full_update_author(self):
        author = create_author(
            user=self.user,
            name='testAuthor',
            date_of_birth='2023-01-01',
            country='Turkey',
            biography='Test Biography'
        )
        payload = {
            'name': 'testAuthorUpdate',
            'date_of_birth': '2023-01-02',
            'country': 'Spain',
            'biography': 'New Biography'
        }
        
        url = detail_author_url(author.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        author.refresh_from_db()
        self.assertEqual(author.user, self.user)

    def test_partial_update_author(self):
        name = 'Test Author Update'
        author = create_author(
            user=self.user,
            name=name,
            country='Turkey'
        )
        payload = {
            'country': 'Spain'
        }

        url = detail_author_url(author.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        author.refresh_from_db()
        self.assertEqual(author.name, name)
        self.assertEqual(author.country, payload['country'])
        self.assertEqual(author.user, self.user)

    def test_delete_author(self):
        author = create_author(user=self.user)

        url = detail_author_url(author.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)