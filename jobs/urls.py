from django.urls import path
from .views import (
    job_list_view,
    job_detail_view,
    create_job_view,
    my_jobs_view,
    edit_job_view,
    delete_job_view,
)

app_name = "jobs"

urlpatterns = [
    path("", job_list_view, name="list"),
    path("<int:pk>/", job_detail_view, name="detail"),
    path("create/", create_job_view, name="create"),
    path("my-jobs/", my_jobs_view, name="my_jobs"),
    path("<int:pk>/edit/", edit_job_view, name="edit"),
    path("<int:pk>/delete/", delete_job_view, name="delete"),
]