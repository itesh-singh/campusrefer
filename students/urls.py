from django.urls import path

from .views import edit_student_profile

app_name = "students"

urlpatterns = [
    path("profile/edit/", edit_student_profile, name="edit_profile"),
]