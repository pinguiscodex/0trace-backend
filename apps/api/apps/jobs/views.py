from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from apps.common.api.serializers import EmptySerializer
from apps.common.api.responses import ok

from .models import PersistedJob
from .selectors import job_progress_for_user
from .serializers import PersistedJobSerializer
from apps.common.api.viewsets import EnvelopeReadOnlyModelViewSet


@extend_schema(tags=["jobs"])
class PersistedJobViewSet(EnvelopeReadOnlyModelViewSet):
    serializer_class = PersistedJobSerializer
    queryset = PersistedJob.objects.none()

    def get_queryset(self):
        return PersistedJob.objects.filter(actor_user=self.request.user)


@extend_schema(tags=["jobs"])
class JobProgressView(APIView):
    serializer_class = EmptySerializer

    def get(self, request):
        return ok(job_progress_for_user(request.user))
