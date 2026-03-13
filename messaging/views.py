from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from connections.models import ConnectionRequest
from .models import Message


@login_required
def conversation_view(request, request_id):
    connection_request = get_object_or_404(ConnectionRequest, id=request_id)

    if connection_request.status != ConnectionRequest.Status.ACCEPTED:
        return redirect("core:home")

    if request.user not in [connection_request.student, connection_request.alumni]:
        return redirect("core:home")

    if request.method == "POST":
        content = request.POST.get("content", "").strip()

        if content:
            Message.objects.create(
                request=connection_request,
                sender=request.user,
                content=content,
            )

        return redirect("messaging:conversation", request_id=request_id)

    messages = connection_request.messages.select_related("sender")

    context = {
        "connection_request": connection_request,
        "messages": messages,
    }
    return render(request, "messaging/conversation.html", context)