from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class HandleOrEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = (username or kwargs.get("handle") or kwargs.get("email") or "").lower()
        if not identifier or password is None:
            return None
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(Q(handle=identifier) | Q(email=identifier))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

