from django import forms

from .models import ConnectionRequest


class ConnectionRequestForm(forms.ModelForm):
    class Meta:
        model = ConnectionRequest
        fields = ["request_type", "message"]
        widgets = {
            "request_type": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                    "placeholder": "Write a short, respectful message explaining why you want to connect.",
                }
            ),
        }