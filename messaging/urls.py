from django.urls import path
from .views import conversation_view, inbox_view

app_name = "messaging"

urlpatterns = [
    path("", inbox_view, name="inbox"),
    path("conversation/<int:request_id>/", conversation_view, name="conversation"),
]