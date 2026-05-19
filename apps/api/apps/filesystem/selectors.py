from .models import FileNode


def nodes_for_machine(machine):
    return FileNode.objects.filter(machine=machine).select_related("parent", "owner")

