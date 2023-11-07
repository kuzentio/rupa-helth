from django.db import models


class Email(models.Model):
    OK = 'OK'
    FAIL = 'FAIL'
    to = models.EmailField()
    to_name = models.CharField(max_length=255)
    from_email = models.EmailField()
    from_name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    text_body = models.TextField()
    sender_provider = models.CharField(max_length=100)
