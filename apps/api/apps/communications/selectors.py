from .models import MailRecipientState


def inbox_for_user(user):
    return MailRecipientState.objects.filter(user=user).select_related("message")

