"""
ASGI config for sist_hub_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from chats.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sist_hub_server.settings')

asgi_app = get_asgi_application()

application = ProtocolTypeRouter({ 
    'http': asgi_app,
    "websocket": 
        AuthMiddlewareStack(
            URLRouter(
                ws_urlpatterns
            )
    )
})


# application = ProtocolTypeRouter({ 
#     'http': asgi_app,
#     "websocket": AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter(
#                 ws_urlpatterns
#             )
#         )
#     )
# })
