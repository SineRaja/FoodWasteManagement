from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import EmailUser
from FoodWasteManagementBackend.test_helpers import mock_signup, mock_login
from django.urls import reverse


class UserProfileTests(APITestCase):
    def test_user_profile(self):
        mock_signup(self.client)
        mock_login(self.client)
        url = reverse('user-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['email'], 'sineraja@gmail.com')

    def test_user_profile_edit_invalid_id(self):
        mock_signup(self.client)
        mock_login(self.client)
        url = reverse('user-edit', kwargs={'pk': 4})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Invalid Request')
        self.assertEqual(EmailUser.objects.filter(id=4).count(), 0)

    def test_user_profile_edit_success(self):
        mock_signup(self.client)
        mock_login(self.client)
        url = reverse('user-edit', kwargs={'pk': 1})
        data = {'phone_number': '5678765675'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['first_name'], 'Sine')
        self.assertEqual(EmailUser.objects.filter(id=1).count(), 1)
        self.assertEqual(EmailUser.objects.get(id=1).first_name, 'Sine')
        self.assertEqual(EmailUser.objects.get(id=1).phone_number, '5678765675')
