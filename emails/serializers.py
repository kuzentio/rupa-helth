from rest_framework import serializers

from emails.entities import EmailEntity


class EmailEntitySerializer(serializers.Serializer):
    to = serializers.EmailField(required=True, max_length=255)
    to_name = serializers.CharField(required=True, max_length=255)
    from_email = serializers.EmailField(required=True, max_length=255)
    from_name = serializers.CharField(required=True, max_length=255)
    subject = serializers.CharField(required=True, max_length=255)
    body = serializers.CharField(required=True)

    def create(self, validated_data) -> EmailEntity:
        return EmailEntity(**validated_data)
