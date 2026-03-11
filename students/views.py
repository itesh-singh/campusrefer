from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import StudentProfileForm


@login_required
def edit_student_profile(request):
    if request.user.role != "student":
        return redirect("core:home")

    profile = request.user.student_profile

    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Student profile updated successfully.")
            return redirect("students:edit_profile")
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, "students/edit_profile.html", {"form": form})