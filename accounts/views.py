from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from .forms import UserLoginForm, UserRegisterForm
from .models import User
from core.gmail_service import send_gmail_message


def register_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            full_name = form.cleaned_data["full_name"]

            user = form.save(commit=False)
            user.is_active = False
            user.is_email_verified = False
            user.save()

            if user.role == "student":
                user.student_profile.full_name = full_name
                user.student_profile.save()
            elif user.role == "alumni":
                user.alumni_profile.full_name = full_name
                user.alumni_profile.save()

            try:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                verify_url = request.build_absolute_uri(
                    reverse("accounts:verify_email", kwargs={"uidb64": uid, "token": token})
                )

                subject = "Verify your CampusRefer account"
                body = f"""
                <p>Hi {user.username},</p>
                <p>Thanks for registering on CampusRefer.</p>
                <p>Please verify your email by clicking the link below:</p>
                <p><a href="{verify_url}">{verify_url}</a></p>
                <p>If you did not create this account, you can ignore this email.</p>
                """

                send_gmail_message(user.email, subject, body)

                messages.success(
                    request,
                    "Account created successfully. Please check your email to verify your account.",
                )
            except Exception as e:
                messages.warning(
                    request,
                    "Account created, but verification email could not be sent. Please try again later.",
                )

            return redirect("accounts:login")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_url = request.build_absolute_uri(
                reverse(
                    "accounts:reset_password",
                    kwargs={"uidb64": uid, "token": token},
                )
            )

            subject = "Reset your CampusRefer password"
            body = f"""
            <p>Hi {user.username},</p>
            <p>Click the link below to reset your password:</p>
            <p><a href="{reset_url}">{reset_url}</a></p>
            <p>If you did not request this, you can ignore this email.</p>
            """

            send_gmail_message(user.email, subject, body)
        except User.DoesNotExist:
            pass
        except Exception:
            pass

        messages.success(
            request,
            "If an account with that email exists, a password reset link has been sent.",
        )
        return redirect("accounts:login")

    return render(request, "accounts/forgot_password.html")


def verify_email_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save(update_fields=["is_active", "is_email_verified"])
        messages.success(request, "Email verified successfully. You can now log in.")
        return redirect("accounts:login")

    messages.error(request, "Verification link is invalid or has expired.")
    return redirect("accounts:login")


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


def reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, "Reset link is invalid or has expired.")
        return redirect("accounts:login")

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(
                request,
                "accounts/reset_password.html",
                {"uidb64": uidb64, "token": token},
            )

        user.set_password(password)
        user.save(update_fields=["password"])

        messages.success(request, "Password reset successfully. You can now log in.")
        return redirect("accounts:login")

    return render(
        request,
        "accounts/reset_password.html",
        {"uidb64": uidb64, "token": token},
    )