import requests
import json
import os
from dotenv import load_dotenv
from Arithmeticpd import past_month

load_dotenv()
leet_api_key = os.getenv('Leetify_API_key')
steam_api_key = os.getenv('Steam_API_key')

def pull_leetify_prof(steam_id, leet_api_key):
    headers = {
        '_leetify_key' : leet_api_key
    }
    response = requests.get(
        f"https://api-public.cs-prod.leetify.com/v3/profile/matches?steam64_id={steam_id}",
        headers = headers
    )

    if response.status_code != 200:
        return None

    data = response.json()
    return past_month(data)
