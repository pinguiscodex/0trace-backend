from django.urls import path

from .views import MachineSoftwareView, SkillDefinitionView, SoftwareLevelUpView, SoftwareSelectView, UserSkillProgressView

urlpatterns = [
    path("machines/<uuid:machine_id>/software/", MachineSoftwareView.as_view(), name="machine-software"),
    path("machines/<uuid:machine_id>/software/select/", SoftwareSelectView.as_view(), name="machine-software-select"),
    path("software/<uuid:software_id>/level-up/", SoftwareLevelUpView.as_view(), name="software-level-up"),
    path("skills/", SkillDefinitionView.as_view(), name="skills"),
    path("users/me/skills/", UserSkillProgressView.as_view(), name="user-skills"),
]

