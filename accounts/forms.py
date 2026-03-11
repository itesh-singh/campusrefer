from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                    "placeholder": "Enter username",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                    "placeholder": "Enter email",
                }
            ),
            "role": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                }
            ),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Enter password",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Confirm password",
            }
        )
    )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Enter username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500",
                "placeholder": "Enter password",
            }
        )
    )