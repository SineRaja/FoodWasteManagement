from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import PasswordResetCode
from FoodWasteManagementBackend.test_helpers import mock_signup
from datetime import timedelta
from django.utils import timezone


class PasswordResetVerifiedTests(APITestCase):
    def test_password_reset_verified_no_password(self):
        url = reverse('password-reset-verified', kwargs={'code': '123123'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['password'], ['This field is required.'])
        self.assertEqual(PasswordResetCode.objects.filter(code='123123').count(), 0)

    def test_password_reset_verify_invalid_code(self):
        url = reverse('password-reset-verified', kwargs={'code': '123123'})
        data = {'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Invalid Request')
        self.assertEqual(PasswordResetCode.objects.filter(code='123123').count(), 0)

    def test_password_reset_verify_expired(self):
        mock_signup(self.client)
        url = reverse('password-reset-request', kwargs={'email': 'sineraja@gmail.com'})
        response = self.client.get(url)
        pwd_reset_code = PasswordResetCode.objects.get(user__email='sineraja@gmail.com')
        pwd_code = pwd_reset_code.code
        pwd_reset_code.expiry_time = pwd_reset_code.expiry_time - timedelta(hours=4)
        pwd_reset_code.save()
        url = reverse('password-reset-verified', kwargs={'code': pwd_code})
        data = {'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Password Reset Code Expired')
        self.assertEqual(PasswordResetCode.objects.filter(code=pwd_code).count(), 1)
        self.assertEqual(PasswordResetCode.objects.get(code=pwd_code).expiry_time < timezone.now(), True)

    def test_password_reset_verify_success(self):
        mock_signup(self.client)
        url = reverse('password-reset-request', kwargs={'email': 'sineraja@gmail.com'})
        response = self.client.get(url)
        pwd_code = PasswordResetCode.objects.get(user__email='sineraja@gmail.com').code
        url = reverse('password-reset-verified', kwargs={'code': pwd_code})
        data = {'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'Password reset Successful')
        self.assertEqual(PasswordResetCode.objects.filter(code=pwd_code).count(), 0)
