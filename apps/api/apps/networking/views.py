from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from apps.common.api.responses import accepted, ok
from apps.machines.models import Machine
from apps.software.models import SoftwareFile
from apps.telemetry.models import SecurityEvent
from apps.telemetry.serializers import SecurityEventSerializer

from .models import CrackJob
from .serializers import CrackJobCreateSerializer, CrackJobSerializer, TerminalExecuteSerializer
from .services.crack_service import cancel_crack_job, create_crack_job
from .services.terminal_service import execute_terminal_command
from .services.terminal_history_service import get_terminal_history


@extend_schema(tags=["jobs"])
class CrackJobListCreateView(APIView):
    serializer_class = CrackJobCreateSerializer

    @extend_schema(operation_id="crack_jobs_list", responses={200: CrackJobSerializer(many=True)})
    def get(self, request):
        return ok(CrackJobSerializer(CrackJob.objects.filter(attacker=request.user), many=True).data)

    @extend_schema(request=CrackJobCreateSerializer, responses={202: CrackJobSerializer})
    def post(self, request):
        serializer = CrackJobCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        machine = Machine.objects.get(id=data["attacker_machine_id"], owner=request.user)
        software = None
        if data.get("cracker_software_id"):
            software = SoftwareFile.objects.get(id=data["cracker_software_id"], owner=request.user, machine=machine)
        crack = create_crack_job(user=request.user, attacker_machine=machine, target_ip=data["target_ip"], cracker_software=software, request=request)
        return accepted(CrackJobSerializer(crack).data, request_id=getattr(request, "request_id", ""))


@extend_schema(tags=["jobs"])
class CrackJobDetailView(APIView):
    serializer_class = CrackJobSerializer

    @extend_schema(operation_id="crack_jobs_retrieve", responses={200: CrackJobSerializer})
    def get(self, request, crack_job_id):
        return ok(CrackJobSerializer(CrackJob.objects.get(id=crack_job_id, attacker=request.user)).data)


@extend_schema(tags=["jobs"])
class CrackJobCancelView(APIView):
    serializer_class = CrackJobSerializer

    def post(self, request, crack_job_id):
        return ok(CrackJobSerializer(cancel_crack_job(user=request.user, crack_job=CrackJob.objects.get(id=crack_job_id, attacker=request.user))).data)


@extend_schema(tags=["telemetry"])
class MachineSecurityEventsView(APIView):
    serializer_class = SecurityEventSerializer

    def get(self, request, machine_id):
        machine = Machine.objects.get(id=machine_id, owner=request.user)
        return ok(SecurityEventSerializer(SecurityEvent.objects.filter(machine=machine), many=True).data)


@extend_schema(tags=["machines"])
class TerminalExecuteView(APIView):
    serializer_class = TerminalExecuteSerializer

    @extend_schema(request=TerminalExecuteSerializer, responses={200: dict})
    def post(self, request, machine_id):
        machine = Machine.objects.get(id=machine_id, owner=request.user)
        serializer = TerminalExecuteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return ok(execute_terminal_command(user=request.user, machine=machine, command=serializer.validated_data["command"]))


@extend_schema(tags=["machines"])
class TerminalHistoryView(APIView):
    serializer_class = TerminalExecuteSerializer

    def get(self, request, machine_id):
        machine = Machine.objects.get(id=machine_id, owner=request.user)
        return ok(get_terminal_history(user=request.user, machine=machine))
