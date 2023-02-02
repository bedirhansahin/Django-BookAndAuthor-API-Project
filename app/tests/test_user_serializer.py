from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

LIST_USER_URL = reverse('api_user:list')
CREATE_USER_URL = reverse('api_user:create')
ME_URL = reverse('api_user:me')
TOKEN_URL = reverse('api_user:token')


def create_user(**params):
    """Create new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserAPIViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_create_success(self):
        payload = {
            'email': 'test@example.com',
            'first_name': 'testname',
            'password': 'testpass1234'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_user_create_with_exist_email_error(self):
        """if user create with an email that exist return error"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass1234',
            'first_name': 'testname'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create_password_short_error(self):
        """if user create with a password too short"""
        payload = {
            'email': 'test@example.com',
            'password': '123',
            'first_name': 'testname'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_detail_me_error(self):
        """Test see detail and updating the user profile"""
        payload = {
            'first_name': 'testname',
            'password': 'newpass123'
        }
        res = self.client.patch(ME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_success(self):
        user_details = {
            'first_name': 'testname',
            'email': 'test@example.com',
            'password': 'testpass1234',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test return error if credentials invalid"""
        create_user(email='test@example.com', password='goodpass')

        payload = {
            'email': 'test@example.com',
            'password': 'bad'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error"""
        payload = {
            'email': 'test@example.com',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserAPIViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            first_name='testname',
            password='testpass1234'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

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

    def test_update_authorized_user_profile(self):
        payload = {
            'first_name': 'testname',
            'password': 'newpass123'
        }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertTrue(self.user.check_password, payload['password'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
