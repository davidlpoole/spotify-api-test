from flask import Flask, render_template, request
import bleach
from spotify import (
    get_access_token,
    get_artist_info,
    get_top_tracks,
    get_track_info,
    get_audio_features,
    get_first_artist,
)

from config import CLIENT_ID, CLIENT_SECRET

app = Flask(__name__, static_folder="static")


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
