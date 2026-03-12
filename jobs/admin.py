from django.contrib import admin
from .models import JobPost


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "alumni", "is_active", "created_at")
    list_filter = ("is_active", "company", "location", "created_at")
    search_fields = ("title", "company", "location")