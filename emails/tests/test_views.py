from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from emails.entities import EmailEntity


class TestEmailView(TestCase):
    def setUp(self) -> None:
        self.data = {
            "to": "sender@example.com",
            "to_name": "Mr. Fake",
            "from_email": "receiver@example.com",
            "from_name": "Ms. Fake",
            "subject": "A Message from Ms. Fake",
            "body": "<p>This is a test message from Ms. Fake.</p>",
        }

    def test_email_view_for_not_allowed_methods(self):
        response = self.client.get(reverse('emails-list'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(reverse('emails-list'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.patch(reverse('emails-list'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(reverse('emails-list'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('emails.services.EmailService.send')
    def test_email_view_validation(self, send_mock):
        response = self.client.post(reverse('emails-list'), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            'to': ['This field is required.'],
            'to_name': ['This field is required.'],
            'from_email': ['This field is required.'],
            'from_name': ['This field is required.'],
            'subject': ['This field is required.'],
            'body': ['This field is required.'],
        })
        self.assertFalse(send_mock.called)

    @patch('emails.services.EmailService.send')
    def test_email_view_calls_send_method(self, send_mock):
        response = self.client.post(reverse('emails-list'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(send_mock.called)
        send_mock.assert_called_once_with(EmailEntity(**self.data))
