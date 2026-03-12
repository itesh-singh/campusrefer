from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


DARK_INPUT = "w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-orange-500 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:placeholder:text-slate-400"


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": DARK_INPUT,
                "placeholder": "Enter full name",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("full_name", "username", "email", "role", "password1", "password2")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": DARK_INPUT,
                    "placeholder": "Enter username (no spaces)",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": DARK_INPUT,
                    "placeholder": "Enter email",
                }
            ),
            "role": forms.Select(
                attrs={
                    "class": DARK_INPUT,
                }
            ),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": DARK_INPUT,
                "placeholder": "Enter password",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": DARK_INPUT,
                "placeholder": "Confirm password",
            }
        )
    )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": DARK_INPUT,
                "placeholder": "Enter username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": DARK_INPUT,
                "placeholder": "Enter password",
            }
        )
    )