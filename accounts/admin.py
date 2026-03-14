from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Role Information", {"fields": ("role", "is_email_verified")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Role Information", {"fields": ("email", "role")}),
    )

    list_display = (
        "username",
        "email",
        "role",
        "is_email_verified",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = (
        "role",
        "is_email_verified",
        "is_staff",
        "is_active",
        "date_joined",
    )
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)