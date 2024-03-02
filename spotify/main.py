import bleach
import pandas as pd

from config import CLIENT_ID, CLIENT_SECRET
from spotify_api import (
    get_access_token,
    get_artist_info,
    get_top_tracks,
    get_track_info,
    get_audio_features,
    get_first_artist,
)


def display_artist_data(artist_name):
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)

    if not access_token:
        print("Failed to retrieve access token.")

    else:
        artist_id = get_first_artist(bleach.clean(artist_name), access_token)
        artist_details = get_artist_info(artist_id, access_token)
        top_tracks = get_top_tracks(artist_id, access_token)

        desired_features = [
            "track_name",
            "danceability",
            "energy",
            "loudness",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
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
                            "track_name": track_name,
                            **audio_features,
                        }
                    )

            # Create DataFrame
            audio_features_df = pd.DataFrame(audio_features_list)

            # Perform some basic EDA (Exploratory Data Analysis)
            summary_statistics = audio_features_df.describe()

            # Output the DataFrame and summary statistics
            print(audio_features_df.loc[:, desired_features])
            print(summary_statistics)


if __name__ == "__main__":
    artist_name = input("Enter the artist name: ")
    if not artist_name:
        artist_name = "Geju"
    display_artist_data(artist_name)
