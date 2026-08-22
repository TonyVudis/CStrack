import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('Leetify_API_key')

def pull_leetify_prof(steam_id, api_key):
    headers = {
        '_leetify_key' : api_key
    }
    response = requests.get(
        f"https://api-public.cs-prod.leetify.com/v3/profile/matches?steam64_id={steam_id}",
        headers = headers
    )
    data = response.json()
    #print(json.dumps(data, indent = 2))

pull_leetify_prof('76561198892933566', api_key)

