from django import forms
from .models import JobPost


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = [
            "title",
            "company",
            "location",
            "job_type",
            "description",
            "apply_link",
            "deadline",
            "is_active",
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Backend Developer Intern",
            }),
            "company": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Microsoft",
            }),
            "location": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Bangalore / Remote",
            }),
            "job_type": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Full-time / Internship / Remote",
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "rows": 6,
                "placeholder": "Write the full job details here",
            }),
            "apply_link": forms.URLInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "https://...",
            }),
            "deadline": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "h-4 w-4 rounded border-slate-300 text-orange-500 focus:ring-orange-500",
            }),
        }