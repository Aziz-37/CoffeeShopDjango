import json
import pytest
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from CoffeeShop.asgi import application
from channels.db import database_sync_to_async

User = get_user_model()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_support_consumer_auth_success():
    user = await database_sync_to_async(User.objects.create_user)(
        username="testuser", password="testpass", email="test@example.com", is_verified=True
    )
    token = str(AccessToken.for_user(user))

    communicator = WebsocketCommunicator(application, "/ws/support/")
    connected, subprotocol = await communicator.connect()
    assert connected

    message_data = {
        "token": token,
        "message": "Hello, support!"
    }
    await communicator.send_json_to(message_data)
    response = await communicator.receive_json_from()
    assert response.get("status") == "success"
    assert response.get("message") == "Hello, support!"

    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_support_consumer_auth_failure():

    communicator = WebsocketCommunicator(application, "/ws/support/")
    connected, subprotocol = await communicator.connect()
    assert connected

    message_data = {
        "token": "invalidtoken",
        "message": "Hello, support!"
    }
    await communicator.send_json_to(message_data)
    response = await communicator.receive_json_from()

    assert "error" in response

    await communicator.disconnect()
