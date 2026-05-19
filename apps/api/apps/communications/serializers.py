from rest_framework import serializers

from .models import MailMessage, MailRecipientState, Notification


class MailMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailMessage
        fields = "__all__"


class MailRecipientStateSerializer(serializers.ModelSerializer):
    message = MailMessageSerializer()

    class Meta:
        model = MailRecipientState
        fields = "__all__"


class MailSendSerializer(serializers.Serializer):
    to_handle = serializers.SlugField()
    subject = serializers.CharField(max_length=160)
    body = serializers.CharField()


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

