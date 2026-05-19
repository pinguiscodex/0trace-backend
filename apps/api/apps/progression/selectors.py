from .models import TutorialMissionDefinition


def active_tutorials():
    return TutorialMissionDefinition.objects.filter(active=True)

