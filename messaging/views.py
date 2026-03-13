from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from connections.models import ConnectionRequest


@login_required
def conversation_view(request, request_id):
    connection_request = get_object_or_404(ConnectionRequest, id=request_id)

    if connection_request.status != ConnectionRequest.Status.ACCEPTED:
        return redirect("core:home")

    if request.user not in [connection_request.student, connection_request.alumni]:
        return redirect("core:home")

    connection_request.messages.exclude(sender=request.user).filter(is_read=False).update(
        is_read=True,
        seen_at=timezone.now(),
    )

    chat_messages = connection_request.messages.select_related("sender")

    context = {
        "connection_request": connection_request,
        "chat_messages": chat_messages,
    }
    return render(request, "messaging/conversation.html", context)


@login_required
def inbox_view(request):
    accepted_requests = ConnectionRequest.objects.filter(
        status=ConnectionRequest.Status.ACCEPTED,
    ).filter(
        Q(student=request.user) | Q(alumni=request.user)
    ).select_related(
        "student",
        "alumni",
        "student__student_profile",
        "alumni__alumni_profile",
    )

    conversations = []

    for req in accepted_requests:
        last_message = req.messages.order_by("-created_at").first()
        other_user = req.alumni if req.student == request.user else req.student
        unread_count = req.messages.exclude(sender=request.user).filter(is_read=False).count()

        conversations.append({
            "request_obj": req,
            "other_user": other_user,
            "last_message": last_message,
            "unread_count": unread_count,
        })

    conversations.sort(
        key=lambda item: item["last_message"].created_at if item["last_message"] else item["request_obj"].created_at,
        reverse=True,
    )

    return render(
        request,
        "messaging/inbox.html",
        {"conversations": conversations},
    )