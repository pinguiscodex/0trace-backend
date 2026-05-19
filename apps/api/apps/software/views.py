from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.common.api.responses import ok
from apps.machines.models import Machine

from .models import SkillDefinition, SkillProgress, SoftwareFile
from .serializers import SkillDefinitionSerializer, SkillProgressSerializer, SoftwareFileSerializer, SoftwareSelectSerializer
from .services.software_leveling_service import level_up_software
from .services.software_selection_service import select_software


@extend_schema(tags=["software"])
class MachineSoftwareView(APIView):
    serializer_class = SoftwareFileSerializer

    def get(self, request, machine_id):
        machine = Machine.objects.get(id=machine_id, owner=request.user)
        return ok(SoftwareFileSerializer(machine.software_files.all(), many=True).data)


@extend_schema(tags=["software"])
class SoftwareSelectView(APIView):
    serializer_class = SoftwareSelectSerializer

    @extend_schema(request=SoftwareSelectSerializer, responses={200: dict})
    def post(self, request, machine_id):
        machine = Machine.objects.get(id=machine_id, owner=request.user)
        serializer = SoftwareSelectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        selection = select_software(user=request.user, machine=machine, **serializer.validated_data)
        return ok({"id": str(selection.id), "app_slug": selection.app_slug, "software_file_id": str(selection.software_file_id)})


@extend_schema(tags=["software"])
class SoftwareLevelUpView(APIView):
    serializer_class = SoftwareFileSerializer

    def post(self, request, software_id):
        software = SoftwareFile.objects.get(id=software_id, owner=request.user)
        return ok(SoftwareFileSerializer(level_up_software(user=request.user, software_file=software)).data)


@extend_schema(tags=["software"])
class SkillDefinitionView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SkillDefinitionSerializer

    def get(self, request):
        return ok(SkillDefinitionSerializer(SkillDefinition.objects.all(), many=True).data)


@extend_schema(tags=["software"])
class UserSkillProgressView(APIView):
    serializer_class = SkillProgressSerializer

    def get(self, request):
        return ok(SkillProgressSerializer(SkillProgress.objects.filter(user=request.user).select_related("skill"), many=True).data)
