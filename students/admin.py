from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "year", "branch", "target_role")
    list_filter = ("year", "branch")
    search_fields = (
        "full_name",
        "user__username",
        "user__email",
        "branch",
        "target_role",
        "skills",
    )