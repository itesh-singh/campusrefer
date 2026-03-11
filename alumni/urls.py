from django.urls import path

from .views import edit_alumni_profile

app_name = "alumni"

urlpatterns = [
    path("profile/edit/", edit_alumni_profile, name="edit_profile"),
]