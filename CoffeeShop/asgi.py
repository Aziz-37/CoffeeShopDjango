import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path
from chat.consumers import SupportConsumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CoffeeShop.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/support/", SupportConsumer.as_asgi()),
        ])
    ),
})
