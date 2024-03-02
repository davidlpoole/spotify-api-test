import os
import requests
import time

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

# Access environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


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


def get_artist_info(artist_id, access_token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        artist_info = response.json()
        return artist_info
    else:
        print("Failed to retrieve artist information.")
        return None


access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)

if access_token:
    print(access_token)
    artist_id = "3F3I57bH1shH7osXaQL1H0"  # Replace with your desired artist ID
    artist_info = get_artist_info(artist_id, access_token)
    if artist_info:
        print("Artist information:", artist_info)
