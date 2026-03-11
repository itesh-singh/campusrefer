from django.urls import path

from .views import (
    create_job_view,
    delete_job_view,
    edit_job_view,
    job_detail_view,
    job_list_view,
    my_jobs_view,
)

app_name = "jobs"

urlpatterns = [
    path("", job_list_view, name="list"),
    path("create/", create_job_view, name="create"),
    path("my-jobs/", my_jobs_view, name="my_jobs"),
    path("<int:pk>/", job_detail_view, name="detail"),
    path("<int:pk>/edit/", edit_job_view, name="edit"),
    path("<int:pk>/delete/", delete_job_view, name="delete"),
]