from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from apps.common.api.responses import ok

from .models import MailMessage, MailRecipientState, Notification
from .serializers import MailRecipientStateSerializer, MailSendSerializer, NotificationSerializer
from .services.mail_service import recipient_from_handle, send_mail
from .services.notification_service import mark_all_read, mark_read


@extend_schema(tags=["communications"])
class MailMessageListCreateView(APIView):
    serializer_class = MailSendSerializer

    @extend_schema(operation_id="mail_messages_list", responses={200: MailRecipientStateSerializer(many=True)})
    def get(self, request):
        return ok(MailRecipientStateSerializer(MailRecipientState.objects.filter(user=request.user).select_related("message"), many=True).data)

    @extend_schema(request=MailSendSerializer, responses={201: dict})
    def post(self, request):
        serializer = MailSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipient = recipient_from_handle(serializer.validated_data["to_handle"])
        message = send_mail(sender=request.user, recipients=[recipient], subject=serializer.validated_data["subject"], body=serializer.validated_data["body"])
        return ok({"message_id": str(message.id)}, status_code=201)


@extend_schema(tags=["communications"])
class MailMessageDetailView(APIView):
    serializer_class = MailRecipientStateSerializer

    @extend_schema(operation_id="mail_messages_retrieve", responses={200: MailRecipientStateSerializer})
    def get(self, request, message_id):
        return ok(MailRecipientStateSerializer(MailRecipientState.objects.get(message_id=message_id, user=request.user)).data)


@extend_schema(tags=["communications"])
class MailReplyView(APIView):
    serializer_class = MailSendSerializer

    @extend_schema(request=MailSendSerializer, responses={201: dict})
    def post(self, request, message_id):
        parent = MailMessage.objects.get(id=message_id)
        serializer = MailSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipient = recipient_from_handle(serializer.validated_data["to_handle"])
        message = send_mail(sender=request.user, recipients=[recipient], subject=serializer.validated_data["subject"], body=serializer.validated_data["body"], parent=parent)
        return ok({"message_id": str(message.id)}, status_code=201)


@extend_schema(tags=["communications"])
class MailMarkReadView(APIView):
    serializer_class = MailRecipientStateSerializer

    def post(self, request, message_id):
        state = MailRecipientState.objects.get(message_id=message_id, user=request.user)
        state.read_at = timezone.now()
        state.save()
        return ok(MailRecipientStateSerializer(state).data)


@extend_schema(tags=["communications"])
class MailMarkUnreadView(APIView):
    serializer_class = MailRecipientStateSerializer

    def post(self, request, message_id):
        state = MailRecipientState.objects.get(message_id=message_id, user=request.user)
        state.read_at = None
        state.save()
        return ok(MailRecipientStateSerializer(state).data)


@extend_schema(tags=["communications"])
class NotificationListView(APIView):
    serializer_class = NotificationSerializer

    def get(self, request):
        return ok(NotificationSerializer(Notification.objects.filter(user=request.user), many=True).data)


@extend_schema(tags=["communications"])
class NotificationMarkReadView(APIView):
    serializer_class = NotificationSerializer

    def post(self, request, notification_id):
        return ok(NotificationSerializer(mark_read(Notification.objects.get(id=notification_id, user=request.user), request.user)).data)


@extend_schema(tags=["communications"])
class NotificationMarkAllReadView(APIView):
    serializer_class = NotificationSerializer

    def post(self, request):
        mark_all_read(request.user)
        return ok({"marked_read": True})
