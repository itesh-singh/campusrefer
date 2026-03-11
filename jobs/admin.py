from django.contrib import admin

from .models import JobPost


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ("company", "role", "location", "alumni", "last_date", "created_at")
    list_filter = ("location", "created_at", "last_date")
    search_fields = ("company", "role", "location")