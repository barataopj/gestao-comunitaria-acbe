from django.urls import path
from . import views

app_name = "solicitacoes"
urlpatterns = [
    path("", views.listar, name="listar"),
    path("nova/", views.criar, name="criar"),
    path("<int:pk>/status/", views.atualizar_status, name="atualizar_status"),
]
