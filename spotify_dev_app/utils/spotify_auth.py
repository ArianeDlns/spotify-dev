import os

import spotipy
import yaml
from spotipy.oauth2 import SpotifyOAuth


def get_spotify_auth():
    """
    Get spotify authentication
    Returns:
        spotipy.Spotify: spotify object with authentication
        username (str): spotify username
    """
    with open("credentials.yml") as f:
        credentials = yaml.load(f, Loader=yaml.FullLoader)

    # Set up the Spotify API
    client_id = credentials["client_id"]  # YOUR_CLIENT_ID
    client_secret = credentials["client_secret"]  # YOUR_CLIENT_SECRET
    username = credentials["username"]  # YOUR_USERNAME

    # Set global variables
    os.environ["SPOTIPY_CLIENT_ID"] = client_id
    os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
    os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8090/callback"

    # Set up the Spotify API
    scope = ['playlist-read-private', 'playlist-read-collaborative']
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return sp, username
