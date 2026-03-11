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
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Enter full name",
            }),
            "batch_year": forms.NumberInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Enter batch year",
            }),
            "branch": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Enter branch",
            }),
            "current_company": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Enter current company",
            }),
            "current_role": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Enter current role",
            }),
            "city": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Enter city",
            }),
            "linkedin_url": forms.URLInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "https://linkedin.com/in/username",
            }),
            "bio": forms.Textarea(attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "rows": 4,
                "placeholder": "Write a short professional summary",
            }),
            "open_to_mentorship": forms.CheckboxInput(attrs={
                "class": "h-4 w-4 rounded border-slate-300 text-orange-500 focus:ring-orange-500",
            }),
            "open_to_referrals": forms.CheckboxInput(attrs={
                "class": "h-4 w-4 rounded border-slate-300 text-orange-500 focus:ring-orange-500",
            }),
        }