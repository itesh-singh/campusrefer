from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings

from .forms import UserLoginForm, UserRegisterForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"]
            user = form.save(commit=False)
            user.is_active = False  # deactivate until email verified
            user.save()

            if user.role == "student":
                user.student_profile.full_name = full_name
                user.student_profile.save()
            elif user.role == "alumni":
                user.alumni_profile.full_name = full_name
                user.alumni_profile.save()

            # Send verification email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = request.build_absolute_uri(
                f"/accounts/verify-email/{uid}/{token}/"
            )

            send_mail(
                subject="Verify your CampusRefer account",
                message=f"Hi {user.username},\n\nPlease verify your email by clicking the link below:\n\n{verification_link}\n\nThis link will expire shortly.\n\nThanks,\nCampusRefer Team",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            messages.success(request, "Account created! Please check your email to verify your account.")
            return redirect("accounts:login")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def verify_email_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        login(request, user)
        messages.success(request, "Email verified successfully! Welcome to CampusRefer.")
        return redirect("core:home")
    else:
        messages.error(request, "Verification link is invalid or has expired.")
        return redirect("accounts:login")


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            messages.error(self.request, "Please verify your email before logging in.")
            return redirect("accounts:login")
        messages.success(self.request, "Logged in successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return "/"


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, "Logged out successfully.")
        return redirect("accounts:login")


# Password Reset Views
def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
                f"/accounts/reset-password/{uid}/{token}/"
            )
            send_mail(
                subject="Reset your CampusRefer password",
                message=f"Hi {user.username},\n\nClick the link below to reset your password:\n\n{reset_link}\n\nIf you didn't request this, ignore this email.\n\nThanks,\nCampusRefer Team",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
        except User.DoesNotExist:
            pass  # Don't reveal if email exists

        messages.success(request, "If that email exists, a reset link has been sent.")
        return redirect("accounts:login")

    return render(request, "accounts/forgot_password.html")


def reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if not user or not default_token_generator.check_token(user, token):
        messages.error(request, "Reset link is invalid or has expired.")
        return redirect("accounts:login")

    if request.method == "POST":
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, "accounts/reset_password.html")

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, "accounts/reset_password.html")

        user.set_password(password)
        user.save()
        messages.success(request, "Password reset successfully! Please log in.")
        return redirect("accounts:login")

    return render(request, "accounts/reset_password.html")