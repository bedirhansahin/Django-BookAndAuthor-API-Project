from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


def create_user(email='test@example.com', first_name='testname', password='pass1234'):
    """Create a new User"""
    return get_user_model().objects.create_user(email, first_name, password)


class CreateUserTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_email_normalized(self):
        email_examples = [
            ['test1@example.COM', 'test1@example.com'],
            ['TEST2@example.com', 'TEST2@example.com'],
            ['test3@EXAMPLE.COM', 'test3@example.com'],
            ['TEST4@EXAMPLE.COM', 'TEST4@example.com']
        ]

        for email, normalized in email_examples:
            user = get_user_model().objects.create_user(email=email, first_name='testname', password='test1234')
            self.assertEqual(user.email, normalized)

    def test_create_user_successful(self):
        # Test Create User
        email = 'test@example.com'
        first_name = 'testname'
        password = 'pass1234'
        user = get_user_model().objects.create_user(
            email=email,
            first_name=first_name,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertTrue(user.check_password(password))

    def test_create_superuser_successful(self):
        # Test Create Superuser
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            first_name='testname',
            password='test1234'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_user_without_email_error(self):
        # Test If there is no email
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='',
                password='test1234')


LIST_USER_URL = reverse('api_user:list')
CREATE_USER_URL = reverse('api_user:create')
ME_URL = reverse('api_user:me')


class UserAPIViewTests(TestCase):

    def test_list_user_success(self):
        payload = {
            'id': 1,
            'first_name': 'testname',
            'last_name': 'testlastname',
            'email': 'test@example.com',
            'is_active': 'True',
            'is_staff': 'False',
            'date_joined': '01/01/2000 00:00:00'

        }
        res = self.client.get(LIST_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
