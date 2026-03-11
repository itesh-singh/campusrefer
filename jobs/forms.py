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
            "company": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Company name",
            }),
            "role": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Job role",
            }),
            "location": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Location",
            }),
            "salary_range": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "e.g. 6-10 LPA",
            }),
            "last_date": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
            }),
            "apply_link": forms.URLInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "https://...",
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "rows": 5,
                "placeholder": "Write job details",
            }),
        }