from django import forms

from .models import JobApplication, JobPost


DARK_INPUT = "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:placeholder:text-slate-400"
DARK_TEXTAREA = "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:placeholder:text-slate-400"


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
                "class": DARK_INPUT,
                "placeholder": "Backend Developer Intern",
            }),
            "company": forms.TextInput(attrs={
                "class": DARK_INPUT,
                "placeholder": "Microsoft",
            }),
            "location": forms.TextInput(attrs={
                "class": DARK_INPUT,
                "placeholder": "Bangalore / Remote",
            }),
            "job_type": forms.TextInput(attrs={
                "class": DARK_INPUT,
                "placeholder": "Full-time / Internship / Remote",
            }),
            "description": forms.Textarea(attrs={
                "class": DARK_TEXTAREA,
                "rows": 6,
                "placeholder": "Write the full job details here",
            }),
            "apply_link": forms.URLInput(attrs={
                "class": DARK_INPUT,
                "placeholder": "https://...",
            }),
            "deadline": forms.DateInput(attrs={
                "type": "date",
                "class": DARK_INPUT,
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "h-4 w-4 rounded border-slate-300 text-orange-500 focus:ring-orange-500 dark:border-slate-600 dark:bg-slate-800",
            }),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ["resume", "cover_letter"]
        widgets = {
            "resume": forms.ClearableFileInput(attrs={
                "class": DARK_INPUT,
            }),
            "cover_letter": forms.Textarea(attrs={
                "class": DARK_TEXTAREA,
                "rows": 5,
                "placeholder": "Write a short cover letter (optional)",
            }),
        }