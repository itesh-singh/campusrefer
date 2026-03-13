import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

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

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "").strip()

        if not message:
            return

        saved_message = await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": saved_message.content,
                "sender_username": saved_message.sender.username,
                "sender_id": saved_message.sender_id,
                "created_at": saved_message.created_at.strftime("%b %d %H:%M"),
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "sender_username": event["sender_username"],
                    "sender_id": event["sender_id"],
                    "created_at": event["created_at"],
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
        )