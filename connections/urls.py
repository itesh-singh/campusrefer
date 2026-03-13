from django.urls import path

from .views import (
    cancel_request_view,
    incoming_requests_view,
    send_connection_request,
    sent_requests_view,
    update_request_status,
)

app_name = "connections"

urlpatterns = [
    path("send/<int:alumni_id>/", send_connection_request, name="send"),
    path("incoming/", incoming_requests_view, name="incoming_requests"),
    path("sent/", sent_requests_view, name="sent_requests"),
    path("update/<int:request_id>/<str:status>/", update_request_status, name="update_status"),
    path("cancel/<int:request_id>/", cancel_request_view, name="cancel_request"),
]