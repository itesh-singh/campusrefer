from django.contrib import admin
from .models import ConnectionRequest


@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ("student", "alumni", "request_type", "status", "created_at")
    list_filter = ("request_type", "status", "created_at")
    search_fields = (
        "student__username",
        "student__email",
        "alumni__username",
        "alumni__email",
        "message",
    )
    ordering = ("-created_at",)