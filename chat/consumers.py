import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from users.models import CustomUser
from .models import SupportMessage

class SupportConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            token = data.get('token')
            user = await self.get_user(token)

            if user.is_authenticated:
                message = data.get('message')
                # Сохраняем сообщение в БД
                await self.save_message(user, message)
                await self.send(text_data=json.dumps({
                    'status': 'success',
                    'message': message
                }))
            else:
                await self.send(text_data=json.dumps({'error': 'Пользователь не аутентифицирован.'}))
        except Exception as e:
            await self.send(text_data=json.dumps({'error': str(e)}))

    @database_sync_to_async
    def get_user(self, token):
        from rest_framework_simplejwt.tokens import AccessToken
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            return CustomUser.objects.get(id=user_id)
        except Exception:
            return AnonymousUser()

    @database_sync_to_async
    def save_message(self, user, text):
        SupportMessage.objects.create(user=user, text=text)
