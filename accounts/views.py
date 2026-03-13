from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

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
            user.is_active = False
            user.save()

            if user.role == "student":
                user.student_profile.full_name = full_name
                user.student_profile.save()
            elif user.role == "alumni":
                user.alumni_profile.full_name = full_name
                user.alumni_profile.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            verify_url = request.build_absolute_uri(
                reverse(
                    "accounts:verify_email",
                    kwargs={"uidb64": uid, "token": token},
                )
            )

            print("VERIFY URL:", verify_url)

            send_mail(
                "Verify your CampusRefer account",
                f"Hi {user.username},\n\nVerify your account:\n{verify_url}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )

            messages.success(
                request,
                "Account created. Please verify your email before logging in.",
            )
            return redirect("accounts:login")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def verify_email_view(request, uidb64, token):
    print("VERIFY VIEW HIT", uidb64, token)
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print("USER FOUND", user.username)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        print("TOKEN VALID")
        user.is_active = True
        user.is_email_verified = True
        user.save(update_fields=["is_active", "is_email_verified"])
        messages.success(request, "Email verified successfully. You can now log in.")
        return redirect("accounts:login")

    print("TOKEN INVALID")
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