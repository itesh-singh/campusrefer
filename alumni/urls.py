from django.urls import path
from .views import (
    alumni_detail,
    alumni_list_view,
    edit_alumni_profile,
    toggle_save_alumni,
    saved_alumni_view,
)

app_name = "alumni"

urlpatterns = [
    path("profile/edit/", edit_alumni_profile, name="edit_profile"),
    path("", alumni_list_view, name="list"),
    path("<int:pk>/", alumni_detail, name="detail"),
    path("<int:pk>/save/", toggle_save_alumni, name="save_toggle"),
    path("saved/", saved_alumni_view, name="saved"),
]