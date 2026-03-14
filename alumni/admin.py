from django.contrib import admin
from .models import AlumniProfile, SavedAlumni


@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "batch_year",
        "branch",
        "current_company",
        "current_role",
        "city",
        "is_verified",
        "profile_views",
    )
    list_filter = (
        "is_verified",
        "open_to_mentorship",
        "open_to_referrals",
        "batch_year",
        "branch",
        "current_company",
        "city",
    )
    search_fields = (
        "full_name",
        "user__username",
        "user__email",
        "branch",
        "current_company",
        "current_role",
        "city",
    )
    ordering = ("full_name",)


@admin.register(SavedAlumni)
class SavedAlumniAdmin(admin.ModelAdmin):
    list_display = ("student", "alumni_profile", "saved_at")
    list_filter = ("saved_at",)
    search_fields = ("student__username", "student__email", "alumni_profile__full_name")
    ordering = ("-saved_at",)