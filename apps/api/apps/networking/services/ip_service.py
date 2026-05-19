from apps.machines.models import Machine


def resolve_fictional_ip(address: str):
    return Machine.objects.filter(fictional_ip=address, active=True).first()

