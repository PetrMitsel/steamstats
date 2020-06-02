from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views
app_name='stats'

urlpatterns = [
    path("", views.login, name="login"),
    path("home", views.index, name="index"),
    path("game/<int:appid>", views.game_detail, name="game_detail"),
    path('logout', login_required(views.LogoutView.as_view(), login_url='/login'), name='logout')
]
