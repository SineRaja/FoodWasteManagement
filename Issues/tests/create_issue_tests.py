from rest_framework import status
from rest_framework.test import APITestCase
from FoodWasteManagementBackend.test_helpers import *


class CreateIssueTests(APITestCase):
    def test_create_issue_without_login(self):
        mock_signup(self.client)
        url = reverse('issue-create')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')

    def test_create_issue_no_data(self):
        mock_signup(self.client)
        mock_login(self.client)
        url = reverse('issue-create')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'issue_title': ['This field is required.'], 'issue_type': ['This field is required.'],
                          'issue_description': ['This field is required.'], 'request': ['This field is required.']})

    def test_create_issue_incorrect_request(self):
        mock_signup(self.client)
        mock_login(self.client)
        url = reverse('issue-create')
        data = {'issue_title': 'issue', 'issue_type': 'type', 'issue_description': 'description', 'request': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['request'], ['Invalid pk "1" - object does not exist.'])
