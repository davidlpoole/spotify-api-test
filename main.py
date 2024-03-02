import os
import requests
import time
from dotenv import load_dotenv
from flask import Flask, render_template, request
import bleach

load_dotenv()

# Access environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

app = Flask(__name__, static_folder="static")


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
    url = f"https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": search_term, "type": "artist", "limit": 1}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        artists = response.json()["artists"]["items"]
        if artists:
            return artists[0]["id"]
        else:
            print("No artists found.")
            return None
    else:
        print("Failed to retrieve artists.")
        return None


def get_top_tracks(artist_id, access_token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["tracks"]
    else:
        print("Failed to retrieve top tracks.")
        return None


def get_track_info(track_id, access_token):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["name"]
    else:
        print("Failed to retrieve top tracks.")
        return None


def get_artist_info(artist_id, access_token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["name"]
    else:
        print("Failed to retrieve top tracks.")
        return None


def get_audio_features(track_id, access_token):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve audio features for track {track_id}.")
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    if access_token:
        if request.method == "POST":
            artist_name = bleach.clean(request.form.get("artist_name"))
            artist_id = get_first_artist(artist_name, access_token)
        else:
            artist_id = "3F3I57bH1shH7osXaQL1H0"

        artist_details = get_artist_info(artist_id, access_token)
        top_tracks = get_top_tracks(artist_id, access_token)
        desired_features = [
            "Danceability",
            "Energy",
            "Loudness",
            "Speechiness",
            "Acousticness",
            "Instrumentalness",
            "Liveness",
            "Valence",
            "Tempo",
        ]

        audio_features_list = []
        if top_tracks:
            for track in top_tracks:
                track_id = track["id"]
                track_name = get_track_info(track_id, access_token)
                audio_features = get_audio_features(track_id, access_token)
                if audio_features:
                    audio_features_list.append(
                        {
                            "track_id": track_id,
                            "track_name": track_name,
                            "features": audio_features,
                        }
                    )
            return render_template(
                "index.html",
                artist_details=artist_details,
                audio_features_list=audio_features_list,
                desired_features=desired_features,
            )
        else:
            return "Failed to retrieve access token."


if __name__ == "__main__":
    app.run(debug=True)
