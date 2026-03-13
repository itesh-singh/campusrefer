import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

from connections.models import ConnectionRequest
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.request_id = self.scope["url_route"]["kwargs"]["request_id"]
        self.room_group_name = f"chat_{self.request_id}"
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        is_allowed = await self.user_can_access_conversation()
        if not is_allowed:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

        await self.mark_messages_as_read()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "read_receipt_update",
            },
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get("type", "chat_message")

        if event_type == "chat_message":
            message = data.get("message", "").strip()

            if not message:
                return

            saved_message = await self.save_message(message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message_id": saved_message.id,
                    "message": saved_message.content,
                    "sender_username": saved_message.sender.username,
                    "sender_id": saved_message.sender_id,
                    "created_at": saved_message.created_at.strftime("%b %d %H:%M"),
                },
            )

        elif event_type == "mark_read":
            await self.mark_messages_as_read()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "read_receipt_update",
                },
            )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_message",
                    "message_id": event["message_id"],
                    "message": event["message"],
                    "sender_username": event["sender_username"],
                    "sender_id": event["sender_id"],
                    "created_at": event["created_at"],
                }
            )
        )

    async def read_receipt_update(self, event):
        last_seen_message_id = await self.get_last_seen_message_id_for_current_user()

        await self.send(
            text_data=json.dumps(
                {
                    "type": "read_receipt_update",
                    "last_seen_message_id": last_seen_message_id,
                }
            )
        )

    @sync_to_async
    def user_can_access_conversation(self):
        try:
            connection_request = ConnectionRequest.objects.get(id=self.request_id)
        except ConnectionRequest.DoesNotExist:
            return False

        if connection_request.status != ConnectionRequest.Status.ACCEPTED:
            return False

        return self.user in [connection_request.student, connection_request.alumni]

    @sync_to_async
    def save_message(self, content):
        connection_request = ConnectionRequest.objects.get(id=self.request_id)
        return Message.objects.create(
            request=connection_request,
            sender=self.user,
            content=content,
            is_read=False,
            seen_at=None,
        )

    @sync_to_async
    def mark_messages_as_read(self):
        Message.objects.filter(
            request_id=self.request_id,
            is_read=False,
        ).exclude(
            sender=self.user,
        ).update(
            is_read=True,
            seen_at=timezone.now(),
        )

    @sync_to_async
    def get_last_seen_message_id_for_current_user(self):
        last_seen = Message.objects.filter(
            request_id=self.request_id,
            sender=self.user,
            is_read=True,
        ).order_by("-created_at").first()

        return last_seen.id if last_seen else None