from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import JobProgressView, PersistedJobViewSet

router = DefaultRouter()
router.register("jobs", PersistedJobViewSet, basename="job")

urlpatterns = router.urls + [
    path("jobs/progress/", JobProgressView.as_view(), name="job-progress"),
]

