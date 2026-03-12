from django import forms
from .models import ConnectionRequest


class ConnectionRequestForm(forms.ModelForm):
    class Meta:
        model = ConnectionRequest
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                    "placeholder": "Hello, I am a student interested in your career path and would appreciate guidance.",
                }
            )
        }