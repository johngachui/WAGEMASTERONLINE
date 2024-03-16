"""
ASGI config for wagemaster_online project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

from fastapi import FastAPI
from django.core.asgi import get_asgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagemaster_online.settings')
django_asgi_app = get_asgi_application()

fastapi_app = FastAPI()

@fastapi_app.get("/hello")
async def read_fastapi():
    return {"message": "Hello from FastAPI"}

from starlette.routing import Mount, Route
from starlette.applications import Starlette

application = Starlette(routes=[
    Mount("/api", app=fastapi_app),
    Mount("/", app=django_asgi_app),
])
