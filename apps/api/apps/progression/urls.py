from django.urls import path

from .views import AchievementListView, TutorialCompleteStepView, TutorialListView

urlpatterns = [
    path("achievements/", AchievementListView.as_view(), name="achievements"),
    path("tutorials/", TutorialListView.as_view(), name="tutorials"),
    path("tutorials/<uuid:mission_id>/complete-step/", TutorialCompleteStepView.as_view(), name="tutorial-complete-step"),
]

