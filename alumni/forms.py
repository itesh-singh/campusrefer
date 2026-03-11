from django import forms

from .models import AlumniProfile


class AlumniProfileForm(forms.ModelForm):
    class Meta:
        model = AlumniProfile
        fields = [
            "full_name",
            "batch_year",
            "branch",
            "current_company",
            "current_role",
            "city",
            "linkedin_url",
            "open_to_mentorship",
            "open_to_referrals",
            "bio",
        ]