from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification


def create_notification(*, user, message, link=""):
    notification = Notification.objects.create(
        user=user,
        message=message,
        link=link,
    )

    try:
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"notifications_{user.id}",
            {
                "type": "send_notification",
                "category": "notification",
                "message": notification.message,
                "link": notification.link,
                "unread_count": user.notifications.filter(is_read=False).count(),
                "created_at": notification.created_at.isoformat(),
            },
        )
    except Exception:
        pass

    return notification