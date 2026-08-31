import requests
import json
import os
from dotenv import load_dotenv
from Arithmeticpd import past_month, steamaccsort

load_dotenv()
leet_api_key = os.getenv('Leetify_API_key')
steam_api_key = os.getenv('Steam_API_key')

def pull_leetify_prof(steam_id, leet_api_key):
    headers = {
        '_leetify_key' : leet_api_key
    }
    leetresponse = requests.get(
        f"https://api-public.cs-prod.leetify.com/v3/profile/matches?steam64_id={steam_id}",
        headers = headers
    )

    if leetresponse.status_code != 200:
        return "There has been a issue getting your leetify information, try making your account public"

    leetdata = leetresponse.json()
    return past_month(leetdata)

def pull_steam_prof(steam_id, steam_api_key):
    steamresponse = requests.get(
        f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_api_key}&steamids={steam_id}"
    )

    if steamresponse.status_code != 200:
        return "There has been a issue with getting your steam information, try making your account public"

    datasteam = steamresponse.json()
    return steamaccsort(datasteam)
