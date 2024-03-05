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
    recs = get_recommendations(seeds_object)
    recs_df = pd.DataFrame(recs["tracks"])

    result_df = pd.DataFrame(
        {
            "album_type": recs_df.album.apply(lambda x: x["album_type"]),
            "artists": recs_df.album.apply(
                lambda x: ", ".join([artist["name"] for artist in x["artists"]])
            ),
            "track_name": recs_df.name,
            "open_spotify_url": recs_df.external_urls.apply(lambda x: x["spotify"]),
            # "preview_url": recs_df.preview_url,
        }
    )

    print(result_df)


if __name__ == "__main__":
    main()
