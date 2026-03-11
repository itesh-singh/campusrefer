from django import forms

from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            "full_name",
            "year",
            "branch",
            "skills",
            "target_role",
            "resume",
            "bio",
        ]