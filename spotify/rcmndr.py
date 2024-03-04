import bleach
import pandas as pd


from spotify_api import (
    get_first_artist,
    get_recommendations,
)


if __name__ == "__main__":
    artist_list = ["Geju", "Merkaba"]

    artist_id_list = []
    for artist_name in artist_list:
        result = get_first_artist(artist_name)

        if result:
            artist_id_list.append(result[0])

    # create a seed object from artist list
    seeds_object = {"seed_artists": ",".join(artist_id_list)}

    recommendations = get_recommendations(seeds_object)
    recommendations_df = pd.DataFrame(recommendations["tracks"])

    # print each row of recommendations_df
    for index, row in recommendations_df.iterrows():
        print(row)
        print("\n")
