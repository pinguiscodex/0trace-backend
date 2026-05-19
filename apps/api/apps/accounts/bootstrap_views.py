from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.common.api.serializers import EmptySerializer
from apps.common.api.responses import ok
from apps.progression.models import TutorialMissionDefinition
from apps.progression.serializers import TutorialCompleteStepSerializer, UserTutorialProgressSerializer
from apps.progression.services.tutorial_service import complete_step

from .services.bootstrap_service import bootstrap_context


@extend_schema(tags=["bootstrap"])
class BootstrapView(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmptySerializer

    def get(self, request):
        return ok(bootstrap_context(request.user))


@extend_schema(tags=["bootstrap"])
class BootstrapCompleteTutorialStepView(APIView):
    serializer_class = TutorialCompleteStepSerializer

    @extend_schema(request=TutorialCompleteStepSerializer, responses={200: UserTutorialProgressSerializer})
    def post(self, request):
        serializer = TutorialCompleteStepSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mission = TutorialMissionDefinition.objects.get(slug=request.data.get("mission_slug", "first-steps"))
        progress = complete_step(user=request.user, mission=mission, step_key=serializer.validated_data["step_key"])
        return ok(UserTutorialProgressSerializer(progress).data)
