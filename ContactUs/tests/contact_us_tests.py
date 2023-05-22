from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ContactUs.models import ContactUs
from FoodWasteManagementBackend.test_helpers import mock_signup


def mock_contact_us(client):
    url = reverse('create-contact-us')
    data = {'email': 'sineraja@gmail.com', 'name': 'Sine Raja', 'phone_no': '6786786786',
            'subject': 'This is subject', 'message': 'Message'}
    response = client.post(url, data, format='json')
    return response


class ContactUsTests(APITestCase):
    def test_create_contact_us_response_no_data(self):
        url = reverse('create-contact-us')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_contact_us_response(self):
        response = mock_contact_us(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactUs.objects.all().count(), 1)

    def test_contact_us_fetch_all(self):
        mock_contact_us(self.client)
        url = reverse('create-contact-us')
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(ContactUs.objects.all().count(), 1)
        mock_contact_us(self.client)
        mock_contact_us(self.client)
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 3)
        self.assertEqual(ContactUs.objects.all().count(), 3)

    def test_contact_us_fetch_detail_invalid_ic(self):
        mock_contact_us(self.client)
        url = reverse('retrieve-contact-us', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_contact_us_fetch_detail(self):
        mock_contact_us(self.client)
        url = reverse('retrieve-contact-us', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['name'], 'Sine Raja')
