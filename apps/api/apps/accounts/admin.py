from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    ordering = ("handle",)
    list_display = ("handle", "email", "display_name", "is_active", "is_staff", "date_joined")
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("handle", "email", "display_name")
    readonly_fields = ("id", "date_joined", "last_login", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("id", "handle", "email", "display_name", "password")}),
        ("Preferences", {"fields": ("preferred_language", "timezone", "onboarding_completed_at", "terms_accepted_at")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("handle", "email", "display_name", "password1", "password2", "is_staff", "is_superuser"),
            },
        ),
    )

