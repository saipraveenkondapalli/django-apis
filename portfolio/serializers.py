from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message', 'site']


class ResumeApiParamSerializer(serializers.Serializer):
    key = serializers.UUIDField(required=True, error_messages={"invalid": 'Not a valid resume key'})
    site = serializers.UUIDField(required=True, error_messages={"invalid": 'Not a valid site key'})


class JobApplicationMessageSerializer(serializers.Serializer):
    message_id = serializers.CharField(required=True, error_messages={"invalid": 'Not a valid message id'})
