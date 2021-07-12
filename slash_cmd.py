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
    json = {
        "name": "spotify",
        "description": "Search for songs on spotify.",
        "options": [
            {
                "name": "song",
                "description": "The name of the song.",
                "type": 3,
                "required": True,
            },
            {
                "name": "artist",
                "description": "The artist of the song.",
                "type": 3,
                "required": False,
            },
        ],
    }

    headers = {"Authorization": f"Bearer {get_token()}"}

    r = requests.post(url, headers=headers, json=json)

    print(r.json())


add_cmd()
