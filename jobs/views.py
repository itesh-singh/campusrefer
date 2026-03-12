from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import JobPostForm
from .models import JobPost


@login_required
def job_list_view(request):
    jobs = JobPost.objects.filter(is_active=True).select_related("alumni")
    return render(request, "jobs/job_list.html", {"jobs": jobs})


@login_required
def job_detail_view(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    return render(request, "jobs/job_detail.html", {"job": job})


@login_required
def create_job_view(request):
    if request.user.role != "alumni":
        messages.error(request, "Only alumni can create job posts.")
        return redirect("jobs:list")

    if request.method == "POST":
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.alumni = request.user
            job.save()
            messages.success(request, "Job post created successfully.")
            return redirect("jobs:my_jobs")
    else:
        form = JobPostForm()

    return render(request, "jobs/create_job.html", {"form": form})


@login_required
def my_jobs_view(request):
    if request.user.role != "alumni":
        messages.error(request, "Only alumni can manage job posts.")
        return redirect("jobs:list")

    jobs = JobPost.objects.filter(alumni=request.user)
    return render(request, "jobs/my_jobs.html", {"jobs": jobs})


@login_required
def edit_job_view(request, pk):
    if request.user.role != "alumni":
        messages.error(request, "Only alumni can edit job posts.")
        return redirect("jobs:list")

    job = get_object_or_404(JobPost, pk=pk, alumni=request.user)

    if request.method == "POST":
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job post updated successfully.")
            return redirect("jobs:my_jobs")
    else:
        form = JobPostForm(instance=job)

    return render(request, "jobs/edit_job.html", {"form": form, "job": job})


@login_required
def delete_job_view(request, pk):
    if request.user.role != "alumni":
        messages.error(request, "Only alumni can delete job posts.")
        return redirect("jobs:list")

    job = get_object_or_404(JobPost, pk=pk, alumni=request.user)

    if request.method == "POST":
        job.delete()
        messages.success(request, "Job post deleted successfully.")
        return redirect("jobs:my_jobs")

    return render(request, "jobs/delete_job.html", {"job": job})