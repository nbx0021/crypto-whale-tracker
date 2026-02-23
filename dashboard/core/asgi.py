import os
import django
from django.core.asgi import get_asgi_application

# 1. First, tell Django where the settings are
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 2. Second, initialize Django (this loads INSTALLED_APPS)
django.setup()

# 3. Third, NOW we can safely import Channels and our specific routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import tracker.routing

# 4. Finally, build the application router
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            tracker.routing.websocket_urlpatterns
        )
    ),
})