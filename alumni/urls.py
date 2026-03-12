from django.urls import path

from .views import alumni_detail, alumni_list_view, edit_alumni_profile

app_name = "alumni"

urlpatterns = [
    path("profile/edit/", edit_alumni_profile, name="edit_profile"),
    path("", alumni_list_view, name="list"),
    path("<int:pk>/", alumni_detail, name="detail"),
]