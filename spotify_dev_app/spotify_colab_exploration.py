import urllib.request

import cv2
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from colorthief import ColorThief
from PIL import Image
from utils.image_handler import (create_color_image, crop_img_to_round,
                                 img_to_html)
from utils.spotify_auth import get_spotify_auth
from utils.spotify_load_data import (createPlaylistInfo,
                                     getCollaborativePlaylists)
from utils.spotify_plots import createRadarChart

# ----------------------------------------------------------------------------------------------------------------------
# To run locally run: 'streamlit run spotify_dev_app/spotify_colab_exploration.py'
# ----------------------------------------------------------------------------------------------------------------------
# DEFAULTS
attributs_DFLT = ['acousticness', 'danceability', 'energy',
                  'instrumentalness', 'liveness', 'speechiness', 'valence', 'mode']

# Load data


@st.cache
def load_data(sp, playlist: str = None, username: str = None):
    try:
        timestamp = pd.Timestamp.now().strftime('%Y%m%d')
        df = pd.read_csv(f'./data/{timestamp}_{playlist}.csv')
    except:
        df = createPlaylistInfo(sp, username, playlist)
    return df


sp, username = get_spotify_auth()
collab_dict = getCollaborativePlaylists(sp, username)
# ----------------------------------------------------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------------------------------------------------

st.sidebar.image("https://i.gifer.com/Nt6v.gif")
st.sidebar.title("Spotify Collaborative Playlist Analysis")
# select
st.sidebar.subheader("Select Playlist")
playlist = st.sidebar.selectbox("Playlist", collab_dict.keys())

df_playlist = load_data(sp, playlist=collab_dict[playlist], username=username)
df_stats = df_playlist.groupby('added_by').mean()

attributes = st.sidebar.multiselect(
    "Attributes:", df_stats.columns[:], attributs_DFLT)
users = st.sidebar.multiselect(
    "Users:", df_stats.index.values, df_stats.index.values)

# ----------------------------------------------------------------------------------------------------------------------
# MAIN PANEL
# ----------------------------------------------------------------------------------------------------------------------

st.title('Spotify Playlist Analysis')

#st.warning("This app is a work in progress. Please feel free to reach out with any questions or comments.")
# two columns
col1, col2 = st.columns(2)

col1.markdown(
    f"<h2 style='text-align: center; color: grey;'>{sp.user(users[0])['display_name']}</h2>", unsafe_allow_html=True)
# col1.write(sp.user(users[0])['display_name'])
try:
    urllib.request.urlretrieve(
        sp.user(users[0])['images'][0]['url'], f"img/users/{users[0]}.jpg")
    dominant_color = create_color_image(
        f"img/users/{users[0]}.jpg", f"img/users/{users[0]}.png")
    col1.markdown("<p style='text-align: center; color: grey;'>" +
                  img_to_html(f"img/users/{users[0]}.png")+"</p>", unsafe_allow_html=True)
except:
    dominant_color = create_color_image(None, "img/user_out.png")
    col1.markdown("<p style='text-align: center; color: grey;'>" +
                  img_to_html("img/user_out.png")+"</p>", unsafe_allow_html=True)


fig = createRadarChart(df_stats, attributes, users[0], color=dominant_color)
col1.plotly_chart(fig, use_container_width=True)
col1.write(f"Tracks added by {sp.user(users[0])['display_name']}")
col1.dataframe(df_playlist.query(f"added_by == '{users[0]}'").iloc[:, 0:4])

col2.markdown(
    f"<h2 style='text-align: center; color: grey;'>{sp.user(users[1])['display_name']}</h2>", unsafe_allow_html=True)
# col2.write(sp.user(users[1])['display_name'])
try:
    urllib.request.urlretrieve(
        sp.user(users[1])['images'][0]['url'], f"img/users/{users[1]}.jpg")
    dominant_color = create_color_image(
        f"img/users/{users[1]}.jpg", f"img/users/{users[1]}.png")
    col2.markdown("<p style='text-align: center; color: grey;'>" +
                  img_to_html(f"img/users/{users[1]}.png")+"</p>", unsafe_allow_html=True)
except:
    dominant_color = create_color_image(None, "img/user_out.png")
    col2.markdown("<p style='text-align: center; color: grey;'>" +
                  img_to_html("img/user_out.png")+"</p>", unsafe_allow_html=True)


fig = createRadarChart(df_stats, attributes, users[1], color=dominant_color)
col2.plotly_chart(fig, use_container_width=True)
col2.write(f"Tracks added by {sp.user(users[1])['display_name']}")
col2.dataframe(df_playlist.query(f"added_by == '{users[1]}'").iloc[:, 0:4])

st.write("## Playlist full tracks")
st.dataframe(df_playlist.iloc[:, 0:4])
