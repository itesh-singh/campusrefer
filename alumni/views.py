from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AlumniProfileForm
from .models import AlumniProfile
from django.core.paginator import Paginator


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

    context = {
        "alumni_profiles": page_obj,
        "page_obj": page_obj,
        "query": query,
        "company": company,
        "city": city,
        "branch": branch,
        "mentorship": mentorship,
        "referral": referral,
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

    return render(request, "alumni/alumni_detail.html", {"profile": profile})