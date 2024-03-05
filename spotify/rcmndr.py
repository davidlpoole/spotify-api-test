import pandas as pd


from spotify_api import (
    create_seeds_object,
    get_artist_ids,
    get_recommendations,
)


def main():
    artist_list = ["Geju", "Merkaba"]
    artist_id_list = get_artist_ids(artist_list)
    seeds_object = create_seeds_object(artist_id_list)
    recommendations = get_recommendations(seeds_object)
    recommendations_df = pd.DataFrame(recommendations["tracks"])

    # print each row of recommendations_df
    for index, row in recommendations_df.iterrows():
        print(row)
        print("\n")


if __name__ == "__main__":
    main()
