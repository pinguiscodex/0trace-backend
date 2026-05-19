from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.api.responses import no_content, ok
from apps.machines.models import Machine

from .models import FileNode
from .serializers import FileMoveCopySerializer, FileNodeCreateSerializer, FileNodeSerializer, FilePermissionSerializer
from .services.file_service import copy_node, create_node, move_node, update_file
from .services.permission_service import ensure_permission, update_permissions


def owned_machine(user, machine_id):
    return Machine.objects.get(id=machine_id, owner=user)


@extend_schema(tags=["filesystem"])
class MachineFileNodesView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FileNodeCreateSerializer

    @extend_schema(responses={200: FileNodeSerializer(many=True)})
    def get(self, request, machine_id):
        machine = owned_machine(request.user, machine_id)
        return ok(FileNodeSerializer(machine.file_nodes.all(), many=True).data)

    @extend_schema(request=FileNodeCreateSerializer, responses={201: FileNodeSerializer})
    def post(self, request, machine_id):
        machine = owned_machine(request.user, machine_id)
        serializer = FileNodeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        node = create_node(machine=machine, user=request.user, **serializer.validated_data)
        return ok(FileNodeSerializer(node).data, status_code=201)


@extend_schema(tags=["filesystem"])
class FileNodeDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FileNodeSerializer

    def get_node(self, user, node_id):
        node = FileNode.objects.select_related("machine").get(id=node_id, machine__owner=user)
        ensure_permission(node, user)
        return node

    @extend_schema(responses={200: FileNodeSerializer})
    def get(self, request, node_id):
        return ok(FileNodeSerializer(self.get_node(request.user, node_id)).data)

    @extend_schema(request=FileNodeSerializer, responses={200: FileNodeSerializer})
    def patch(self, request, node_id):
        node = update_file(node=self.get_node(request.user, node_id), user=request.user, content=request.data.get("content"), metadata=request.data.get("metadata"))
        return ok(FileNodeSerializer(node).data)

    def delete(self, request, node_id):
        node = self.get_node(request.user, node_id)
        ensure_permission(node, request.user, write=True)
        node.delete()
        return no_content()


@extend_schema(tags=["filesystem"])
class FileMoveView(APIView):
    serializer_class = FileMoveCopySerializer

    @extend_schema(request=FileMoveCopySerializer, responses={200: FileNodeSerializer})
    def post(self, request, node_id):
        serializer = FileMoveCopySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        node = FileNode.objects.get(id=node_id, machine__owner=request.user)
        return ok(FileNodeSerializer(move_node(node=node, user=request.user, new_path=serializer.validated_data["path"])).data)


@extend_schema(tags=["filesystem"])
class FileCopyView(APIView):
    serializer_class = FileMoveCopySerializer

    @extend_schema(request=FileMoveCopySerializer, responses={201: FileNodeSerializer})
    def post(self, request, node_id):
        serializer = FileMoveCopySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        node = FileNode.objects.get(id=node_id, machine__owner=request.user)
        return ok(FileNodeSerializer(copy_node(node=node, user=request.user, new_path=serializer.validated_data["path"])).data, status_code=201)


@extend_schema(tags=["filesystem"])
class FilePermissionView(APIView):
    serializer_class = FilePermissionSerializer

    @extend_schema(request=FilePermissionSerializer, responses={200: FilePermissionSerializer})
    def post(self, request, node_id):
        node = FileNode.objects.get(id=node_id, machine__owner=request.user)
        permissions = update_permissions(node, user=request.user, values=request.data)
        return ok(FilePermissionSerializer(permissions).data)
