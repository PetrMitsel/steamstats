from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from stats.models import Game

import json, urllib, os

api_key = os.environ.get("STEAM_API_KEY")

"""

view functions

"""


def index(request):
    context = {}
    steam_id = 76561198094609550
    context["games"] = get_player_games(steam_id)
    context["recent_games"] = get_recent_games(steam_id)
    context["friends_list"] = get_friends_list(steam_id)
    context["profile_info"] = get_player_profile(steam_id)
    return render(request, "home.html", context)


def game_detail(request, appid):
    context = {}
    context["news_items"] = get_game_news(appid)
    context["game_name"] = get_game_name(appid)
    return render(request, "game_detail.html", context)


"""
steam_api methods
"""


def get_game_news(appid):
    urlobj = urllib.request.urlopen(
        f"http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?key={api_key}&appid={appid}&count=5&maxlength=300&format=json"
    )
    data = json.loads(urlobj.read().decode("utf-8"))
    news_items = data["appnews"]["newsitems"]
    return news_items


def get_game_name(appid):
    game_urlobj = urllib.request.urlopen(
        f"http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={api_key}&appid={appid}"
    )
    game_data = json.loads(game_urlobj.read().decode("utf-8"))
    if game_data["game"].get("gameName", False):
        game_name = game_data["game"]["gameName"]
        return game_name
    else:
        return ""


def get_player_games(steam_id):
    urlobj = urllib.request.urlopen(
        f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json&include_appinfo=true"
    )
    data = json.loads(urlobj.read().decode("utf-8"))
    if data["response"].get("games", False):
        games = data["response"]["games"]
    else:
        games = []
    return games


def get_recent_games(steam_id):
    urlobj = urllib.request.urlopen(
        f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={api_key}&steamid={steam_id}&format=json"
    )
    data = json.loads(urlobj.read().decode("utf-8"))
    recent_games = data["response"]["games"]
    return recent_games


def get_friends_list(steam_id):
    urlobj = urllib.request.urlopen(
        f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steam_id}&relationship=friend"
    )
    data = json.loads(urlobj.read().decode("utf-8"))
    friend_ids = ",".join(
        [friend["steamid"] for friend in data["friendslist"]["friends"]]
    )
    urlobj_2 = urllib.request.urlopen(
        f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={friend_ids}"
    )
    data_2 = json.loads(urlobj_2.read().decode("utf-8"))
    friends_list = data_2["response"]["players"]
    return friends_list


def get_player_profile(steam_id):
    urlobj = urllib.request.urlopen(
        f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}"
    )
    data = json.loads(urlobj.read().decode("utf-8"))
    profile_info = data["response"]["players"][0]
    return profile_info
