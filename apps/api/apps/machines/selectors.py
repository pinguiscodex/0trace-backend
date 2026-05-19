from .models import Machine


def machines_for_user(user):
    return Machine.objects.filter(owner=user)

