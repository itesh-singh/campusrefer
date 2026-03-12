from django import forms

from .models import StudentProfile


DARK_INPUT = "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:placeholder:text-slate-400"
DARK_TEXTAREA = "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:placeholder:text-slate-400"


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
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": DARK_INPUT,
                "placeholder": "Enter full name",
            }),
            "year": forms.NumberInput(attrs={
                "class": DARK_INPUT,
                "placeholder": "Enter current year",
            }),
            "branch": forms.TextInput(attrs={
                "class": DARK_INPUT,
                "placeholder": "Enter branch",
            }),
            "skills": forms.Textarea(attrs={
                "class": DARK_TEXTAREA,
                "rows": 4,
                "placeholder": "Python, Django, PostgreSQL, REST APIs...",
            }),
            "target_role": forms.TextInput(attrs={
                "class": DARK_INPUT,
                "placeholder": "Backend Developer",
            }),
            "bio": forms.Textarea(attrs={
                "class": DARK_TEXTAREA,
                "rows": 4,
                "placeholder": "Write a short profile summary",
            }),
            "resume": forms.ClearableFileInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200",
            }),
        }