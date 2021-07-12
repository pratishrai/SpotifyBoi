import os
import requests
import logging
import time
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

spotify_token = ""
spotify_token_expiry = 0.0

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def get_spotify_token() -> str:
    """
    Return the spotify auth token, update if expired.
    :return: spotify token
    """
    global spotify_token, spotify_token_expiry
    # check if token expired ( - 300 to add buffer of 5 minutes)
    if spotify_token_expiry - 300 > time.time():
        logging.info(f"using spotify token: {spotify_token[:41]}")
        return spotify_token
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
    )
    spotify_token = r.json()["access_token"]
    # token valid for an hour
    spotify_token_expiry = time.time() + 3600
    logging.info(f"updated spotify token: {spotify_token[:41]}")
    return spotify_token


def search_song(query):
    headers = {"Authorization": f"Bearer {get_spotify_token()}"}

    search = requests.get(
        f"https://api.spotify.com/v1/search?query={query}&type=track&limit=1",
        headers=headers,
    ).json()

    name = None
    artist = None
    link = None

    if search["tracks"]["total"] > 0:
        link = search["tracks"]["items"][0]["external_urls"]["spotify"]
        name = search["tracks"]["items"][0]["name"]
        artists = []
        for artist in search["tracks"]["items"][0]["artists"]:
            artists.append(artist["name"])
        return name, artists, link
    else:
        return name, artist, link
