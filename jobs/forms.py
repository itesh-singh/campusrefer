from django import forms

from .models import JobPost


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = [
            "company",
            "role",
            "location",
            "salary_range",
            "last_date",
            "apply_link",
            "description",
        ]
        widgets = {
            "last_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 5}),
        }