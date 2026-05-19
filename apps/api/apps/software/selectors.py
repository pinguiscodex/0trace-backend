from .models import SoftwareFile


def software_for_machine(machine):
    return SoftwareFile.objects.filter(machine=machine, owner=machine.owner)

