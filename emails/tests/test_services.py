from unittest.mock import patch

from django.test import TestCase, override_settings

from django.core.exceptions import ImproperlyConfigured

from emails.entities import EmailEntity
from emails.models import Email
from emails.providers import PostmarkEmailProvider, MailgunEmailProvider
from emails.services import EmailService
from emails.views import email_service


class TestEmailService(TestCase):
    def setUp(self) -> None:
        self.email_data = {
            'to': 'receiver@example.com',
            'to_name': 'Mr. Fake',
            'from_email': 'sender@example.com',
            'from_name': 'Ms. Fake',
            'subject': 'A Message from Ms. Fake',
            'body': '<p>This is a test message from Ms. Fake.</p>',
        }
        self.email = EmailEntity(**self.email_data)

    @override_settings(EMAIL_PROVIDERS=[])
    def test_not_configures_email_providers_raises_exception(self):
        with self.assertRaises(ImproperlyConfigured):
            EmailService()

    @override_settings(EMAIL_PROVIDERS=[{'class': ''}, {'class': ''}])
    def test_wrong_configured_email_providers_build_raises_exception(self):
        with self.assertRaises(ImportError):
            EmailService()

    @override_settings(EMAIL_PROVIDERS=[
        {'class': 'emails.providers.PostmarkEmailProvider'},
        {'class': 'emails.providers.MailgunEmailProvider'}
    ])
    def test_email_service_loads_all_providers(self):
        self.assertEqual(len(email_service.email_providers), 2)
        self.assertIsInstance(email_service.email_providers[0], PostmarkEmailProvider)

    @override_settings(
        EMAIL_PROVIDERS=[
            {'class': 'emails.providers.PostmarkEmailProvider'},
            {'class': 'emails.providers.MailgunEmailProvider'}],
        EMAIL_PERSISTENCE_MODE='all',
    )
    @patch('emails.providers.PostmarkEmailProvider.send')
    @patch('emails.providers.MailgunEmailProvider.send')
    def test_email_service_sends_next_available_if_failed(self, mailgun_mock, postmark_mock):
        postmark_mock.return_value = 'FAIL'
        mailgun_mock.return_value = 'OK'
        email_service.send(self.email)
        self.assertTrue(mailgun_mock.called)
        email = Email.objects.get()
        self.assertEqual(email.sender_provider, MailgunEmailProvider.name)

    def test_converting_html_body_to_plain_text(self):
        html_body = '<html><h1>Example subject.</h1><b>Bold text</b></html>'
        self.assertEqual(email_service._get_text_body(html_body), 'Example subject.Bold text')
