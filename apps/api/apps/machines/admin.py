from django.contrib import admin

from .models import AppDefinition, AppInstall, Machine, MachinePreference, OSDefinition, OSInstall


@admin.register(OSDefinition)
class OSDefinitionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "version", "availability", "cost", "company_site")
    search_fields = ("name", "slug", "company_site")
    list_filter = ("availability", "terminal_style")


@admin.register(AppDefinition)
class AppDefinitionAdmin(admin.ModelAdmin):
    list_display = ("default_display_name", "slug", "category", "is_core", "is_uninstallable")
    search_fields = ("default_display_name", "slug")
    list_filter = ("category", "is_core", "is_uninstallable")


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "hostname", "fictional_ip", "active", "powered_on", "created_at")
    search_fields = ("name", "owner__handle", "hostname", "fictional_ip")
    list_filter = ("active", "powered_on")


admin.site.register(MachinePreference)
admin.site.register(OSInstall)
admin.site.register(AppInstall)

