from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

from .forms import AlumniProfileForm
from .models import AlumniProfile, SavedAlumni


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
    company = request.GET.get("company", "").strip()
    city = request.GET.get("city", "").strip()
    branch = request.GET.get("branch", "").strip()
    mentorship = request.GET.get("mentorship", "")
    referral = request.GET.get("referral", "")

    alumni_profiles = AlumniProfile.objects.select_related("user").all().order_by("full_name")

    if query:
        alumni_profiles = alumni_profiles.filter(
            Q(full_name__icontains=query)
            | Q(current_company__icontains=query)
            | Q(current_role__icontains=query)
            | Q(city__icontains=query)
            | Q(branch__icontains=query)
        )

    if company:
        alumni_profiles = alumni_profiles.filter(current_company__icontains=company)

    if city:
        alumni_profiles = alumni_profiles.filter(city__icontains=city)

    if branch:
        alumni_profiles = alumni_profiles.filter(branch__icontains=branch)

    if mentorship == "yes":
        alumni_profiles = alumni_profiles.filter(open_to_mentorship=True)

    if referral == "yes":
        alumni_profiles = alumni_profiles.filter(open_to_referrals=True)

    paginator = Paginator(alumni_profiles, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # get saved alumni ids for current student
    saved_ids = []
    if request.user.role == "student":
        saved_ids = SavedAlumni.objects.filter(
            student=request.user
        ).values_list("alumni_profile_id", flat=True)

    context = {
        "alumni_profiles": page_obj,
        "page_obj": page_obj,
        "query": query,
        "company": company,
        "city": city,
        "branch": branch,
        "mentorship": mentorship,
        "referral": referral,
        "saved_ids": saved_ids,
    }
    return render(request, "alumni/alumni_list.html", context)


@login_required
def alumni_detail(request, pk):
    profile = get_object_or_404(AlumniProfile, pk=pk)

    if request.user.role == "student":
        AlumniProfile.objects.filter(pk=pk).update(
            profile_views=F("profile_views") + 1
        )
        profile.refresh_from_db()

    is_saved = False
    if request.user.role == "student":
        is_saved = SavedAlumni.objects.filter(
            student=request.user,
            alumni_profile=profile,
        ).exists()

    return render(request, "alumni/alumni_detail.html", {
        "profile": profile,
        "is_saved": is_saved,
    })


@login_required
def toggle_save_alumni(request, pk):
    if request.user.role != "student":
        messages.error(request, "Only students can save alumni.")
        return redirect("alumni:list")

    profile = get_object_or_404(AlumniProfile, pk=pk)
    saved = SavedAlumni.objects.filter(
        student=request.user,
        alumni_profile=profile,
    ).first()

    if saved:
        saved.delete()
        messages.success(request, f"{profile.full_name} removed from saved alumni.")
    else:
        SavedAlumni.objects.create(student=request.user, alumni_profile=profile)
        messages.success(request, f"{profile.full_name} saved successfully!")

    return redirect("alumni:detail", pk=pk)


@login_required
def saved_alumni_view(request):
    if request.user.role != "student":
        messages.error(request, "Only students can view saved alumni.")
        return redirect("core:home")

    saved = SavedAlumni.objects.filter(
        student=request.user
    ).select_related("alumni_profile")

    return render(request, "alumni/saved_alumni.html", {"saved": saved})