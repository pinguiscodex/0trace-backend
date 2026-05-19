from .session_service import session_context


def bootstrap_context(user):
    return session_context(user)

