from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.common.api.responses import ok

from .models import AchievementDefinition, TutorialMissionDefinition, UserAchievement, UserTutorialProgress
from .serializers import (
    AchievementDefinitionSerializer,
    TutorialCompleteStepSerializer,
    TutorialMissionDefinitionSerializer,
    UserAchievementSerializer,
    UserTutorialProgressSerializer,
)
from .services.tutorial_service import complete_step


@extend_schema(tags=["progression"])
class AchievementListView(APIView):
    serializer_class = AchievementDefinitionSerializer

    def get(self, request):
        return ok(
            {
                "definitions": AchievementDefinitionSerializer(AchievementDefinition.objects.filter(active=True), many=True).data,
                "unlocked": UserAchievementSerializer(UserAchievement.objects.filter(user=request.user).select_related("achievement"), many=True).data,
            }
        )


@extend_schema(tags=["progression"])
class TutorialListView(APIView):
    permission_classes = [AllowAny]
    serializer_class = TutorialMissionDefinitionSerializer

    def get(self, request):
        if request.user.is_authenticated:
            return ok(UserTutorialProgressSerializer(UserTutorialProgress.objects.filter(user=request.user).select_related("mission"), many=True).data)
        return ok(TutorialMissionDefinitionSerializer(TutorialMissionDefinition.objects.filter(active=True), many=True).data)


@extend_schema(tags=["progression"])
class TutorialCompleteStepView(APIView):
    serializer_class = TutorialCompleteStepSerializer

    @extend_schema(request=TutorialCompleteStepSerializer, responses={200: UserTutorialProgressSerializer})
    def post(self, request, mission_id):
        serializer = TutorialCompleteStepSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mission = TutorialMissionDefinition.objects.get(id=mission_id)
        return ok(UserTutorialProgressSerializer(complete_step(user=request.user, mission=mission, step_key=serializer.validated_data["step_key"])).data)
