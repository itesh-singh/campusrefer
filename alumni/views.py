from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import AlumniProfileForm


@login_required
def edit_alumni_profile(request):
    if request.user.role != "alumni":
        return redirect("core:home")

    profile = request.user.alumni_profile

    if request.method == "POST":
        form = AlumniProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Alumni profile updated successfully.")
            return redirect("alumni:edit_profile")
    else:
        form = AlumniProfileForm(instance=profile)

    return render(request, "alumni/edit_profile.html", {"form": form})