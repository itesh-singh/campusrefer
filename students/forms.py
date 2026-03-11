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
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Enter full name",
            }),
            "year": forms.NumberInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Enter current year",
            }),
            "branch": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Enter branch",
            }),
            "skills": forms.Textarea(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "rows": 4,
                "placeholder": "Python, Django, PostgreSQL, REST APIs...",
            }),
            "target_role": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Backend Developer",
            }),
            "bio": forms.Textarea(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "rows": 4,
                "placeholder": "Write a short profile summary",
            }),
            "resume": forms.ClearableFileInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3",
            }),
        }