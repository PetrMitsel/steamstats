from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("game/<int:appid>", views.game_detail, name="game_detail"),
]
