from django.urls import path

from .views import (
    MailMarkReadView,
    MailMarkUnreadView,
    MailMessageDetailView,
    MailMessageListCreateView,
    MailReplyView,
    NotificationListView,
    NotificationMarkAllReadView,
    NotificationMarkReadView,
)

urlpatterns = [
    path("mail/messages/", MailMessageListCreateView.as_view(), name="mail-messages"),
    path("mail/messages/<uuid:message_id>/", MailMessageDetailView.as_view(), name="mail-message-detail"),
    path("mail/messages/<uuid:message_id>/reply/", MailReplyView.as_view(), name="mail-message-reply"),
    path("mail/messages/<uuid:message_id>/mark-read/", MailMarkReadView.as_view(), name="mail-message-mark-read"),
    path("mail/messages/<uuid:message_id>/mark-unread/", MailMarkUnreadView.as_view(), name="mail-message-mark-unread"),
    path("notifications/", NotificationListView.as_view(), name="notifications"),
    path("notifications/<uuid:notification_id>/mark-read/", NotificationMarkReadView.as_view(), name="notification-mark-read"),
    path("notifications/mark-all-read/", NotificationMarkAllReadView.as_view(), name="notifications-mark-all-read"),
]

