from django.urls import path

from .views import FileCopyView, FileMoveView, FileNodeDetailView, FilePermissionView, MachineFileNodesView

urlpatterns = [
    path("machines/<uuid:machine_id>/filesystem/nodes/", MachineFileNodesView.as_view(), name="machine-file-nodes"),
    path("files/<uuid:node_id>/", FileNodeDetailView.as_view(), name="file-node-detail"),
    path("files/<uuid:node_id>/move/", FileMoveView.as_view(), name="file-node-move"),
    path("files/<uuid:node_id>/copy/", FileCopyView.as_view(), name="file-node-copy"),
    path("files/<uuid:node_id>/permissions/", FilePermissionView.as_view(), name="file-node-permissions"),
]

