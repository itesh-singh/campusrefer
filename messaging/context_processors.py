from messaging.models import Message


def unread_messages_count(request):
    if not request.user.is_authenticated:
        return {"unread_messages_count": 0}

    count = Message.objects.filter(
        request__status="accepted",
        is_read=False,
    ).exclude(sender=request.user).filter(
        request__student=request.user
    ).count() + Message.objects.filter(
        request__status="accepted",
        is_read=False,
    ).exclude(sender=request.user).filter(
        request__alumni=request.user
    ).count()

    return {"unread_messages_count": count}