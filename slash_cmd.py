import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

url = f"https://discord.com/api/v8/applications/{os.getenv('APPLICATION_ID')}/commands"

API_ENDPOINT = "https://discord.com/api/v8"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def get_token():
    data = {"grant_type": "client_credentials", "scope": "applications.commands.update"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(
        "%s/oauth2/token" % API_ENDPOINT,
        data=data,
        headers=headers,
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    r.raise_for_status()
    return r.json()["access_token"]


def add_cmd():
    json = {"name": "Search on Spotify", "type": 3}

    headers = {"Authorization": f"Bearer {get_token()}"}

    r = requests.post(url, headers=headers, json=json)

    print(r.json())


add_cmd()

# {'id': '943183184235987045', 'application_id': '863282917991120916', 'version': '943183184235987046', 'default_permission': True, 'default_member_permissions': None, 'type': 3, 'name': 'Search on Spotify', 'name_localizations': None, 'description': '', 'description_localizations': None, 'dm_permission': None}
