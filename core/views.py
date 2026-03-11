from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def home_view(request):
    return render(request, "core/home.html")


@login_required
def profile_redirect_view(request):
    if request.user.role == "student":
        return redirect("students:edit_profile")
    if request.user.role == "alumni":
        return redirect("alumni:edit_profile")
    return redirect("core:home")