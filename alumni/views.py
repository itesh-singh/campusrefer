from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AlumniProfileForm
from .models import AlumniProfile


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


@login_required
def alumni_list_view(request):
    query = request.GET.get("q", "").strip()

    alumni_profiles = AlumniProfile.objects.select_related("user").all()

    if query:
        alumni_profiles = alumni_profiles.filter(
            Q(full_name__icontains=query)
            | Q(current_company__icontains=query)
            | Q(current_role__icontains=query)
            | Q(city__icontains=query)
            | Q(branch__icontains=query)
        )

    context = {
        "alumni_profiles": alumni_profiles,
        "query": query,
    }
    return render(request, "alumni/alumni_list.html", context)


@login_required
def alumni_detail_view(request, pk):
    profile = get_object_or_404(AlumniProfile, pk=pk)
    return render(request, "alumni/alumni_detail.html", {"profile": profile})