from rest_framework.throttling import UserRateThrottle


class CommandRateThrottle(UserRateThrottle):
    scope = "commands"

