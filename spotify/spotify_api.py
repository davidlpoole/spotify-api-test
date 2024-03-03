import os
import requests
import time
from dotenv import load_dotenv


def get_access_token():

    access_token_file = "access_token.txt"

    if os.path.exists(access_token_file):
        with open(access_token_file, "r") as file:
            access_token, expires_at = file.read().split(",")
            if time.time() < float(expires_at):
                return access_token

    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        expires_in = response.json()["expires_in"]
        with open(access_token_file, "w") as file:
            file.write(f"{access_token},{time.time() + expires_in}")
        return access_token
    else:
        print("Failed to retrieve access token.")
        return None


def spotify_api_request(url, headers, params=None):
    access_token = get_access_token()
    headers["Authorization"] = f"Bearer {access_token}"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to make API request to {url}.")
        return None


def get_first_artist(search_term):
    url = "https://api.spotify.com/v1/search"
    headers = {"Content-Type": "application/json"}
    params = {"q": search_term, "type": "artist", "limit": 1}
    response_json = spotify_api_request(url, headers, params)
    if response_json:
        artists = response_json.get("artists", {}).get("items", [])
        if artists:
            return artists[0]["id"]
        else:
            print("No artists found.")
            return None
    else:
        return None


def get_top_tracks(artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = {"Content-Type": "application/json"}
    response_json = spotify_api_request(url, headers)
    if response_json:
        return response_json.get("tracks", [])
    else:
        return None


def get_track_info(track_id):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {"Content-Type": "application/json"}
    response_json = spotify_api_request(url, headers)
    if response_json:
        return response_json.get("name")
    else:
        return None


def get_artist_info(artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {"Content-Type": "application/json"}
    response_json = spotify_api_request(url, headers)
    if response_json:
        return response_json.get("name")
    else:
        return None


def get_audio_features(track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {"Content-Type": "application/json"}
    response_json = spotify_api_request(url, headers)
    if response_json:
        return response_json
    else:
        return None
