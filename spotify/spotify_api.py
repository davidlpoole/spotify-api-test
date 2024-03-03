import os
import requests
import time


def make_spotify_request(endpoint, access_token, params=None):
    base_url = "https://api.spotify.com/v1/"
    url = base_url + endpoint
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data from {endpoint}.")
        return None


def get_access_token(client_id, client_secret):
    access_token_file = "access_token.txt"

    if os.path.exists(access_token_file):
        with open(access_token_file, "r") as file:
            access_token, expires_at = file.read().split(",")
            if time.time() < float(expires_at):
                return access_token

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


def get_first_artist(search_term, access_token):
    endpoint = "search"
    params = {"q": search_term, "type": "artist", "limit": 1}
    response = make_spotify_request(endpoint, access_token, params)
    if response:
        artists = response["artists"]["items"]
        if artists:
            return artists[0]["id"]
        else:
            print("No artists found.")
            return None


def get_top_tracks(artist_id, access_token):
    endpoint = f"artists/{artist_id}/top-tracks"
    response = make_spotify_request(endpoint, access_token)
    if response:
        return response["tracks"]


def get_track_info(track_id, access_token):
    endpoint = f"tracks/{track_id}"
    response = make_spotify_request(endpoint, access_token)
    if response:
        return response["name"]


def get_artist_info(artist_id, access_token):
    endpoint = f"artists/{artist_id}"
    response = make_spotify_request(endpoint, access_token)
    if response:
        return response["name"]


def get_audio_features(track_id, access_token):
    endpoint = f"audio-features/{track_id}"
    response = make_spotify_request(endpoint, access_token)
    return response
