import bleach
import pandas as pd

from spotify_api import (
    get_top_tracks,
    get_audio_features,
    get_first_artist,
)


def get_top_tracks_audio_features(artist_name):
    print("Getting data for", artist_name)

    # get the first artist
    [artist_id, artist_name] = get_first_artist(bleach.clean(artist_name))

    # get the top tracks
    top_tracks = get_top_tracks(artist_id)
    top_tracks_df = pd.DataFrame(top_tracks)[["id", "name"]]

    # get the audio features
    all_track_ids = ",".join(top_tracks_df["id"].tolist())
    audio_features = get_audio_features(all_track_ids)["audio_features"]
    audio_features_df = pd.DataFrame(audio_features)

    # join the two dataframes
    top_tracks_df = top_tracks_df.merge(audio_features_df, on="id")

    # add a column which contains artist name
    top_tracks_df["artist"] = artist_name

    return top_tracks_df


if __name__ == "__main__":
    # artist_name = input("Enter the artist name: ")
    artist_list = ["Geju", "Taylor Swift", "Merkaba", "Luke Combs"]

    # Initialize an empty list to hold all DataFrames
    all_artists_data = []

    for artist_name in artist_list:
        # Get the DataFrame for the current artist
        artist_df = get_top_tracks_audio_features(artist_name)

        # append the artist_df to a csv file
        artist_df.to_csv(f"out/{artist_name}.csv", index=False, mode="w")
