from __future__ import annotations

from django.contrib.auth import login, logout
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import User
from apps.machines.services.machine_bootstrap_service import bootstrap_machine_for_user
from apps.telemetry.services.audit_log_service import audit


@transaction.atomic
def signup_user(*, request, handle: str, email: str, password: str, display_name: str = "", terms_accepted: bool = False) -> User:
    user = User.objects.create_user(
        handle=handle,
        email=email,
        password=password,
        display_name=display_name or handle,
        terms_accepted_at=timezone.now() if terms_accepted else None,
    )
    bootstrap_machine_for_user(user)
    audit(actor=user, event_type="signup", request=request, metadata={"handle": user.handle})
    login(request, user)
    return user


def login_user(*, request, user: User) -> None:
    login(request, user)
    audit(actor=user, event_type="login_success", request=request)


def login_failed(*, request, identifier: str) -> None:
    audit(actor=None, event_type="login_failure", request=request, metadata={"identifier": identifier})


def logout_user(*, request) -> None:
    actor = request.user if request.user.is_authenticated else None
    logout(request)
    audit(actor=actor, event_type="logout", request=request)

