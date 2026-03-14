from django.contrib import admin
from .models import JobPost


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "location",
        "job_type",
        "alumni",
        "is_active",
        "deadline",
        "created_at",
    )
    list_filter = (
        "is_active",
        "company",
        "location",
        "job_type",
        "created_at",
        "deadline",
    )
    search_fields = (
        "title",
        "company",
        "location",
        "job_type",
        "description",
        "alumni__username",
        "alumni__email",
    )
    ordering = ("-created_at",)