from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.views import View

from .forms import UserLoginForm, UserRegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"]
            user = form.save()

            if user.role == "student":
                user.student_profile.full_name = full_name
                user.student_profile.save()
            elif user.role == "alumni":
                user.alumni_profile.full_name = full_name
                user.alumni_profile.save()

            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("core:home")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "Logged in successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return "/"


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, "Logged out successfully.")
        return redirect("accounts:login")