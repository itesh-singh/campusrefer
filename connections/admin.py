from django.contrib import admin

from .models import ConnectionRequest


@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ("student", "alumni", "request_type", "status", "created_at")
    list_filter = ("request_type", "status", "created_at")