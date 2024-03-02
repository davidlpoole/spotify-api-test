# Testing the Spotify API

Get audio features of an artists top tracks for further analysis

[Available features](https://developer.spotify.com/documentation/web-api/reference/get-audio-features):
Danceability, Energy, Key, Loudness, Mode, Speechiness, Acousticness, Instrumentalness, Liveness, Valence, Tempo

## Getting Started

### Pre-requisites

Before you can run this project, you need to have the following installed:

- Python3
- pipenv (`pip3 install pipenv`)

### Installation

1. Clone the repository:  
`git clone https://github.com/davidlpoole/spotify-api-test`  
`cd spotify-api-test`

1. Setup the virtual environment:  
`pipenv shell`

1. Install the dependencies:  
`pipenv install`

1. Create a `.env` file from `.env.example` and add your client_id and client_secret from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

### Run the application

`python main.py`

### Recommended for contributors

- Install the [Black Formatter extension](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) in VS Code for Python code formatting.