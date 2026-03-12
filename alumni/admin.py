from django.contrib import admin

from .models import AlumniProfile


@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "batch_year",
        "branch",
        "current_company",
        "current_role",
        "is_verified",
    )
    list_filter = ("is_verified", "batch_year", "branch")