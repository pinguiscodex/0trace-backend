from django.contrib.auth import get_user_model
from django.db import transaction

from apps.communications.models import MailMessage, MailRecipientState


@transaction.atomic
def send_mail(*, sender, recipients, subject: str, body: str, parent=None, system: bool = False):
    message = MailMessage.objects.create(sender=sender, subject=subject, body=body, parent=parent, system=system)
    for recipient in recipients:
        MailRecipientState.objects.get_or_create(message=message, user=recipient)
    return message


def send_system_mail(*, user, subject: str, body: str):
    return send_mail(sender=None, recipients=[user], subject=subject, body=body, system=True)


def recipient_from_handle(handle: str):
    return get_user_model().objects.get(handle=handle.lower())

