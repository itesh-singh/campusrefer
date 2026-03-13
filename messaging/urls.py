from django.urls import path
from .views import conversation_view

app_name = "messaging"

urlpatterns = [
    path("conversation/<int:request_id>/", conversation_view, name="conversation"),
]