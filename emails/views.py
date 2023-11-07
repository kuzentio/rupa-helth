from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from emails.serializers import EmailEntitySerializer
from emails.services import EmailService


email_service = EmailService()


class EmailViewSet(ViewSet):

    def create(self, request, *args, **kwargs):
        serializer = EmailEntitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_entity = serializer.create(serializer.data)
        email_service.send(email_entity)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
