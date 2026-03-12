from django import forms

from .models import ConnectionRequest


DARK_INPUT = "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:placeholder:text-slate-400"
DARK_TEXTAREA = "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:placeholder:text-slate-400"


class ConnectionRequestForm(forms.ModelForm):
    class Meta:
        model = ConnectionRequest
        fields = ["request_type", "message"]
        widgets = {
            "request_type": forms.Select(
                attrs={
                    "class": DARK_INPUT,
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": DARK_TEXTAREA,
                    "placeholder": "Write a short, respectful message explaining why you want to connect.",
                }
            ),
        }