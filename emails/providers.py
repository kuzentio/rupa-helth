import logging

import requests
from requests import Response

from django.conf import settings
from rest_framework import status

from emails.models import Email


logger = logging.getLogger(__name__)


class EmailProvider:
    name: str = None
    api_key: str = None
    api_endpoint: str = None
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    def send(self, email: Email) -> None:
        raise NotImplementedError

    def handle_response(self, response: Response) -> str:
        if response.status_code not in (status.HTTP_200_OK, status.HTTP_201_CREATED):
            logger.error(f'Failed to send email using provider {self.name} - {response.content}')
            return 'FAIL'
        logger.info(f'Email successfully sent using provider {self.name}')
        return 'OK'


class MailgunEmailProvider(EmailProvider):
    name = 'mailgun'
    api_key = settings.MAILGUN_API_KEY
    api_endpoint = settings.MAILGUN_API_ENDPOINT

    def send(self, email: Email) -> str:
        response = requests.post(
            self.api_endpoint,
            auth=('api', self.api_key),
            headers=self.headers,
            data={
                'from': f"{email.from_name} <{email.from_email}>",
                'to': [email.to, ],
                'subject': email.subject,
                'html': email.body,
                'text': email.text_body,
            },
        )
        return self.handle_response(response)


class PostmarkEmailProvider(EmailProvider):
    name = 'postmark'
    api_key = settings.POSTMARK_API_KEY
    api_endpoint = settings.POSTMARK_ENDPOINT

    def send(self, email: Email) -> str:
        response = requests.post(
            self.api_endpoint,
            headers={
                'X-Postmark-Server-Token': self.api_key,
                **self.headers,
            },
            json={
                'From': email.from_email,
                'To': email.to,
                'Subject': email.subject,
                'TextBody': email.text_body,
                'HtmlBody': email.body,
            },
        )

        return self.handle_response(response)
