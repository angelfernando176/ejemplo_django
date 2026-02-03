from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("", views.index, name="index"),
    path("crear/", views.crear_usuario_api, name="crear_usuario"),
]
