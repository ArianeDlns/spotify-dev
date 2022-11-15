import numpy as np
import pandas as pd


def getCollaborativePlaylists(sp, user: str):
    """
    Get collaborative playlists from Spotify
    """
    collab_dict = {}
    playlists = sp.user_playlists(user)
    for playlist in playlists['items']:
        if playlist['collaborative'] or (playlist['owner']['id'] != user and '+' in playlist['name']):
            collab_dict[playlist['name']] = playlist['id']
    return collab_dict


def getTrackIDs(sp, user: str, playlist_id: str):
    """
    Get track ids from a playlist
    Args:
        user (str): spotify username
        playlist_id (str): spotify playlist id
    Returns:
        track_infos (list): list of track infos
    """
    track_infos = []
    playlist = sp.user_playlist(user, playlist_id)
    for idx, item in enumerate(playlist['tracks']['items']):
        track = item['track']
        track_infos.append([track['id'], idx, item['added_by']['id']])
    return track_infos


def getTrackFeatures(sp, id: str):
    """
    Get the audio features for a single track
    Args:
        id: the spotify id of the track
    Returns:
        a dictionary of the audio features
    """
    meta = sp.track(id)
    features = sp.audio_features(id)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    valence = features[0]['valence']
    time_signature = features[0]['time_signature']
    key = features[0]['key']
    mode = features[0]['mode']
    uri = features[0]['uri']

    track = [name, album, artist, release_date,
             length, popularity, acousticness,
             danceability, energy, instrumentalness,
             liveness, loudness, speechiness, tempo,
             valence, time_signature,
             key, mode, uri]
    return track


def createPlaylistInfo(sp, username: str, playlist_id: str):
    """
    Get tracks info from a playlist
    """
    track_infos = getTrackIDs(sp, username, playlist_id)
    features_list = []
    for track_info in track_infos:
        features = getTrackFeatures(sp, track_info[0])
        features_list.append([*features, *track_info[1:]])

    # Create a dataframe from the list of features
    df = pd.DataFrame(features_list, columns=['name', 'album', 'artist', 'release_date',
                                              'length', 'popularity', 'acousticness',
                                              'danceability', 'energy', 'instrumentalness',
                                              'liveness', 'loudness', 'speechiness', 'tempo',
                                              'valence', 'time_signature',
                                              'key', 'mode', 'uri', 'playlist_idx', 'added_by'])
    # save to csv with timestamp
    timestamp = pd.Timestamp.now().strftime('%Y%m%d')
    df.to_csv(f'./data/{timestamp}_{playlist_id}.csv', index=False, encoding='utf-8')
    return df
