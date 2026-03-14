from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "request",
        "sender",
        "is_read",
        "seen_at",
        "created_at",
    )
    list_filter = ("is_read", "created_at", "seen_at")
    search_fields = (
        "sender__username",
        "sender__email",
        "content",
        "request__student__username",
        "request__alumni__username",
    )
    ordering = ("-created_at",)