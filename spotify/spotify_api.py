import os
import requests
import time
from dotenv import load_dotenv


def get_access_token():
    """
    Function to retrieve the access token for accessing the Spotify API.
    It loads the access token from a file and checks if it is expired.
    If the token is expired or doesn't exist, it retrieves a new access token
    by making a request to the Spotify API and saves it to a file.
    Returns the valid access token or None if retrieval fails.
    """
    # Load access token from file
    access_token_file = "access_token.txt"

    # Check if access token is expired
    if os.path.exists(access_token_file):
        with open(access_token_file, "r") as file:
            access_token, expires_at = file.read().split(",")
            if time.time() < float(expires_at):
                return access_token

    # If access token is expired or doesn't exist, retrieve new access token
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

    # Save access token to file
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
    """
    Makes a request to the Spotify API using the provided URL, headers, and optional parameters.
    Returns the JSON response if the request is successful, otherwise returns None.
    """
    # Add access token to headers
    access_token = get_access_token()
    headers["Authorization"] = f"Bearer {access_token}"

    # Make API request
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to make API request to {url}.")
        print(f"Response status code: {response.status_code}")
        return None


def get_artist_ids(artist_list):
    """
    Return a list of artist IDs for the given list of artist names.

    :param artist_list: A list of strings representing artist names.
    :return: A list of artist IDs.
    """
    artist_id_list = []
    for artist_name in artist_list:
        result = get_first_artist(artist_name)

        if result and result[1].lower() == artist_name.lower():
            print(f"{artist_name} found.")
            artist_id_list.append(result[0])
        else:
            print(f"{artist_name} not found.")

    return artist_id_list or None


def create_seeds_object(artist_list):
    seeds_object = {"seed_artists": ",".join(artist_list)}
    return seeds_object


def get_recommendations(
    seeds_object,
):
    """
    Get recommendations for the given seeds object using the Spotify API.

    Args:
        seeds_object (dict): The seeds object containing the artist IDs.

    Returns:
        dict or None: The recommendations if available, or None if not found.
    """
    url = "https://api.spotify.com/v1/recommendations"
    headers = {"Content-Type": "application/json"}
    seeds_object["limit"] = 10
    params = seeds_object
    response_json = spotify_api_request(url, headers, params)
    if response_json:
        return response_json
    else:
        return None


def get_first_artist(search_term):
    """
    Get the first artist ID from Spotify API based on the search term.

    Args:
    - search_term: A string representing the search term.

    Returns:
    - A object containing the artist ID and name, if found, or None if no artists are found.
    """
    url = "https://api.spotify.com/v1/search"
    headers = {"Content-Type": "application/json"}
    params = {"q": search_term, "type": "artist", "limit": 1}
    response_json = spotify_api_request(url, headers, params)
    if response_json:
        artists = response_json.get("artists", {}).get("items", [])
        if artists:
            return [artists[0]["id"], artists[0]["name"]]
        else:
            print("No artists found.")
            return None
    else:
        return None


def get_top_tracks(artist_id):
    """
    Retrieve the top tracks for a given artist ID using the Spotify API.

    Args:
        artist_id (str): The unique identifier for the artist.

    Returns:
        list: A list of top tracks for the specified artist, or None if the request fails.
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = {"Content-Type": "application/json"}
    response_json = spotify_api_request(url, headers)
    if response_json:
        return response_json.get("tracks", [])
    else:
        return None


def get_track_info(track_id):
    """
    Retrieves information about a track from the Spotify API.

    Args:
        track_id (str): The unique identifier for the track.

    Returns:
        str or None: The name of the track if available, or None if the track information is not found.
    """
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {"Content-Type": "application/json"}
    response_json = spotify_api_request(url, headers)
    if response_json:
        return response_json.get("name")
    else:
        return None


def get_artist_info(artist_id):
    """
    Get artist information by artist ID.

    Parameters:
    artist_id (str): The unique identifier of the artist.

    Returns:
    str or None: The name of the artist if available, otherwise None.
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {"Content-Type": "application/json"}
    response_json = spotify_api_request(url, headers)
    if response_json:
        return response_json.get("name")
    else:
        return None


def get_audio_features(track_ids):
    """
    Retrieve audio features of a track from the Spotify API.

    Args:
        track_id (str): The unique identifier of the track.

    Returns:
        dict or None: The audio features of the track if available, or None if not found.
    """
    url = f"https://api.spotify.com/v1/audio-features?ids={track_ids}"
    headers = {"Content-Type": "application/json"}
    response_json = spotify_api_request(url, headers)
    if response_json:
        return response_json
    else:
        return None
