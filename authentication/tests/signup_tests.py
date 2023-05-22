from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import EmailUser
from FoodWasteManagementBackend.test_helpers import mock_signup


class SignUpTests(APITestCase):
    def test_create_account(self):
        url = reverse('signup')
        data = {'first_name': 'Sine', 'last_name': 'Raja', 'email': 'sineraja@gmail.com', 'password': 'password',
                'phone_number': '4564564564', 'user_type': 'DONOR'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmailUser.objects.count(), 1)
        self.assertEqual(EmailUser.objects.get().first_name, 'Sine')

    def test_create_account_already_exists(self):
        mock_signup(self.client)
        url = reverse('signup')
        data = {'first_name': 'Sine', 'last_name': 'Raja', 'email': 'sineraja@gmail.com', 'password': 'password',
                'phone_number': '4564564564', 'user_type': 'DONOR'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['email'], ['user with this email address already exists.'])
        self.assertEqual(EmailUser.objects.count(), 1)
