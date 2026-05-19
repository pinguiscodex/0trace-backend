from .models import Website


def websites_for_user(user):
    return Website.objects.filter(owner=user)

