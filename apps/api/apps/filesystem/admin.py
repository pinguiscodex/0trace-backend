from django.contrib import admin

from .models import FileNode, FilePermission


@admin.register(FileNode)
class FileNodeAdmin(admin.ModelAdmin):
    list_display = ("path", "machine", "owner", "kind", "file_type", "is_system", "created_at")
    list_filter = ("kind", "file_type", "is_hidden", "is_system")
    search_fields = ("path", "name", "owner__handle", "machine__hostname")


admin.site.register(FilePermission)

