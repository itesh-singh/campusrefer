from django.contrib import admin

from .models import ConnectionRequest


@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ("student", "alumni", "status", "created_at")
    list_filter = ("status", "created_at")