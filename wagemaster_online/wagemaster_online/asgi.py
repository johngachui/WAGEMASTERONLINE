"""
ASGI config for wagemaster_online project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# django_app/asgi.py
import os
from django.core.asgi import get_asgi_application
from fastapi_app.main import app as fastapi_app
from starlette.applications import Starlette
from starlette.routing import Mount

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagemaster_online.settings')

django_asgi_app = get_asgi_application()

application = Starlette(routes=[
    Mount("/api", app=fastapi_app),  # Routes /api to FastAPI
    Mount("/", app=django_asgi_app),  # Django handles all other routes
])
