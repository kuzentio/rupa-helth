import logging
import re

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from emails import const
from emails.entities import EmailEntity
from emails.models import Email as EmailModel
from emails.providers import EmailProvider

logger = logging.getLogger(__name__)


class EmailService:
    email_providers = []

    def __init__(self):
        if not settings.EMAIL_PROVIDERS:
            raise ImproperlyConfigured("EMAIL_PROVIDERS configuration is required")

        for email_provider_conf in settings.EMAIL_PROVIDERS:
            self.email_providers.append(self._build_email_provider(email_provider_conf))

    @staticmethod
    def _get_text_body(body):
        return re.compile(r'<.*?>').sub('', body)

    def _to_email_model(self, email: EmailEntity):
        return EmailModel(
            to=email.to,
            to_name=email.to_name,
            from_email=email.from_email,
            from_name=email.from_name,
            subject=email.subject,
            body=email.body,
            text_body=self._get_text_body(email.body),
        )

    def send(self, email_entity: EmailEntity) -> str:
        email = self._to_email_model(email_entity)
        for email_provider in self.email_providers:
            status = email_provider.send(email)

            if status == 'OK':
                self.success_handler(email, email_provider.name)
                break
            logger.info(f'Failed to send email using provider {email_provider}')
        else:
            self.fail_handler(email)

    @staticmethod
    def _build_email_provider(conf: dict) -> EmailProvider:
        provider_class = import_string(conf['class'])

        return provider_class()

    @staticmethod
    def success_handler(email: EmailModel, sender_provider: str) -> None:
        logger.info(f"Email successfully sent by {sender_provider}")
        if settings.EMAIL_PERSISTENCE_MODE == const.EMAIL_PERSISTENCE_MODE_ALL:
            email.sender_provider = sender_provider
            email.save()

    @staticmethod
    def fail_handler(email: EmailModel) -> None:
        email.save()
        logger.error(f"Fail to send email {email.id} with all providers, leave `sender_provider` empty")
        # logger.exception(f"Fail to send email {email.id} with all providers, leave `sender_provider` empty")
