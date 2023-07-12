import spotipy
import os
import time
import sys
import pandas as pd
from spotipy import SpotifyClientCredentials, util, SpotifyOAuth
from dotenv import load_dotenv
import numpy as np
from urllib.request import urlretrieve
from urllib.parse import urlencode


load_dotenv()

# Load HSM
#HSM_model = keras.models.load_model('./HSM')
#HEM_model = keras.models.load_model('./HEM')
#HEE_model = keras.models.load_model('./HEE')

client_id = os.environ['client_ID']
client_secret = os.environ['client_secret']
redirect_uri = os.environ['redirect_url']
username = os.environ['username']
scope = 'playlist-modify-public'

#Credentials to access the Spotify Music Data
manager = SpotifyClientCredentials(client_id,client_secret)

#Credentials to access to  the Spotify User's Playlist, Favorite Songs, etc. 
token = 'BQAtnBY8lZihu6Q7DEk9DIhM424eG9mQMJbgHrfCGtqiVYqVIOL5snRmdRmZGsKisHzyk-HWZZLOugNPZ-lyU-anpDKTxxbVn40j_qeO45UBg8JMoxscFIOpmvfqtvhIREM_JcFU7VuRE-ZAHVXRypzM5zq0epZZnDi4HwdmUm-U0d_xCCwemQy-nDWSHph0SlrPmPAZzjXWF6P6bOeqUTEwM0PCmhEgtqvk4Q' 
sp = spotipy.Spotify(client_credentials_manager=manager, auth=token)

spt = spotipy.Spotify(auth=token)
#sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))



def spotipy_generate_token(user_url):
    load_dotenv()
    api_base = os.environ['api_base']
    client_id = os.environ['client_ID']
    client_secret = os.environ['client_secret']
    redirect_uri = os.environ['redirect_url']
    username = user_url
    scope = 'playlist-modify-public'
    manager='penis'

    # Step 1: Send Authorization request to accounts.sotify.com/authorize



    # Step 2: User logs in and we recieve an authorization code
    # Step 3: Use authorization code to get token
    # Step 4: Pass token into spotipy



    sp = spotipy.Spotify(client_credentials_manager=manager, auth=token)
    return sp



def get_songs_features(ids):

    meta = sp.track(ids)
    features = sp.audio_features(ids)

    # meta
    name = meta['name']
    #genre = meta['genre']
    #album = meta['album']['name']
    #artist = meta['album']['artists'][0]['name']
    #release_date = meta['album']['release_date']
    #popularity = meta['popularity']
    #length = meta['duration_ms']
    ids =  meta['id']
    #uri =  meta['uri']

    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    #instrumentalness = features[0]['instrumentalness']
    #liveness = features[0]['liveness']
    valence = features[0]['valence']
    loudness = features[0]['loudness']
    #speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    #key = features[0]['key']
    #time_signature = features[0]['time_signature']

    track = [[name,  ids, danceability, acousticness, energy, tempo, valence, loudness]]
    columns = ['name', 'ids', 'danceability','acousticness','energy','tempo','valence','loudness']
    preprocessed_data = pd.DataFrame(track, columns=columns)
    return preprocessed_data


def add_song_feature(ids):

    #meta = sp.track(ids)
    features = sp.audio_features(ids)

    # meta
    #name = meta['name']
    #album = meta['album']['name']
    #artist = meta['album']['artists'][0]['name']
    #release_date = meta['album']['release_date']
    #popularity = meta['popularity']
    #length = meta['duration_ms']
    #ids =  meta['id']
    #uri =  meta['uri']

    # features
    #acousticness = features[0]['acousticness']
    #danceability = features[0]['danceability']
    #energy = features[0]['energy']
    #instrumentalness = features[0]['instrumentalness']
    #liveness = features[0]['liveness']
    #valence = features[0]['valence']
    #loudness = features[0]['loudness']
    #speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    #key = features[0]['key']
    #time_signature = features[0]['time_signature']

    track = [[tempo]]
    columns = ['tempo']
    added_feature = pd.DataFrame(track, columns=columns)
    return added_feature


def download_playlist(id_playlist,n_songs):
    tsongs_list = pd.DataFrame()
    data = [[]]
    tracks =[]
    songs_list = []

    for i in range(0,n_songs,100):
        playlist = sp.playlist_tracks(id_playlist,limit=100,offset=i)
        
        for songs in playlist['items']:
            song_id = songs['track']['id']
            name = songs['track']['name']
            songs_list.append(song_id)
            data = [[song_id, name]]
            temp = pd.DataFrame(data, columns=['song_id','name'])
            tsongs_list = pd.concat([tsongs_list, temp])
    
    counter = 1
    for ids in songs_list:
        
        #time.sleep(.1)
        track = get_songs_features(ids)
        name = track['name'][0]
        print(f"Song {counter} Added: {name}")
        #  By {track[2]} from the album {track[1]}
        
        counter+=1
    
    print("Music Downladed!")

    return tsongs_list


def download_user_playlists(username):
    playlists = sp.user_playlists(username)
    playlist_list = pd.DataFrame()
    data = [[]]

    while playlists:
        for i,playlist in enumerate(playlists['items']):
            song_id = playlist['uri'].split(':')[2]
            data = [[song_id, playlist['name']]]
            temp = pd.DataFrame(data, columns=['playlist_id','name'])
            playlist_list = pd.concat([playlist_list, temp])

        if playlists['next']:
            playlists = sp.next(playlists)

        else:
            playlists = None
    return playlist_list



def download_liked_songs():
    print('Now downloading liked songs')
    scope = 'user-library-read'
    token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri) 
    spt = spotipy.Spotify(auth=token)   
    results = spt.current_user_saved_tracks()
    songlist = pd.DataFrame()
    data = [[]] 

    while results:
        for i,result in enumerate(results):
            for item in results['items']:
                track = item['track']
                print("%32.32s %s" % (track['artists'][0]['name'], track['name']))
                song_id = track['id']
                song_name = track['name']
                data = [[song_id, song_name]]
                time.sleep(0.05)
                temp = pd.DataFrame(data, columns=['song_id','name'])
                songlist = pd.concat([songlist, temp])
            if results['next']:
                results = spt.next(results)
            else:
                results = None
                break
    return songlist

'''
def evaluate_stress(preprocessed_dataset):
    properties = list(preprocessed_dataset.columns.values)
    properties.remove('name')
    properties.remove('ids')
    input = np.array(preprocessed_dataset[properties])
    results = np.array([])
    output = HSM_model.predict(input)
    results = np.append(results, [output])
    stress = pd.DataFrame(results.T, columns=['stress'])
    final = pd.concat([preprocessed_dataset,stress.set_index(preprocessed_dataset.index)], axis=1).reset_index(drop=True)
    return final


def evaluate_mood(preprocessed_dataset):
    dfM = pd.DataFrame().assign(danceability=preprocessed_dataset['danceability'], valence=preprocessed_dataset['valence'],acousticness=preprocessed_dataset['acousticness'])
    properties = list(dfM.columns.values)
    input = np.array(dfM[properties])
    results = np.array([])
    output = HEM_model.predict(input)
    results = np.append(results, [output])
    stress = pd.DataFrame(results.T, columns=['mood'])
    final = pd.concat([preprocessed_dataset,stress.set_index(preprocessed_dataset.index)], axis=1).reset_index(drop=True)
    return final


def evaluate_energy(preprocessed_dataset):
    dfE = pd.DataFrame().assign(energy=preprocessed_dataset['energy'], loudness=preprocessed_dataset['loudness'],tempo=preprocessed_dataset['tempo'])
    properties = list(dfE.columns.values)
    input = np.array(dfE[properties])
    results = np.array([])
    output = HEM_model.predict(input)
    results = np.append(results, [output])
    stress = pd.DataFrame(results.T, columns=['energy'])
    final = pd.concat([preprocessed_dataset,stress.set_index(preprocessed_dataset.index)], axis=1).reset_index(drop=True)
    return final
'''

def create_spotipy_playlists():
    print('Now creating playlists')
    spt.user_playlist_create(user=username, name='Spotvac: Happy', public=True, description='A playlist with the lowest stress music')
    time.sleep(0.3)
    print('Playlist Spotvac: Happy Created')
    spt.user_playlist_create(user=username, name='Spotvac: Good Vibes', public=True, description='A playlist with nice, low stress music')
    time.sleep(0.3)
    print('Playlist Spotvac: Good Vibes Created')
    spt.user_playlist_create(user=username, name='Spotvac: Chill Vibes', public=True, description='A playlist with average stress music')
    time.sleep(0.3)
    print('Playlist Spotvac: Chill Vibes Created')
    spt.user_playlist_create(user=username, name='Spotvac: Sad', public=True, description='A playlist with generally high stress music')
    time.sleep(0.3)
    print('Playlist Spotvac: Sad Created')
    spt.user_playlist_create(user=username, name='Spotvac: Depression', public=True, description='A playlist with the highest stress music')
    time.sleep(0.3)
    print('Playlist Spotvac: Depression Created')
    time.sleep(5)
    spotvac_playlist_list = download_user_playlists(username)
    spotvac_playlist_list = spotvac_playlist_list.reset_index(drop=True)
    
    i=0
    for entry in range(len(spotvac_playlist_list)):
        name = spotvac_playlist_list['name'][i]
        if name.startswith('Spotvac'):
            #print(name)
            i+=1
            pass
        else:
            spotvac_playlist_list.drop([i], axis=0, inplace=True)
            #print(f"{name} doesnt start with xd")
            i+=1
    return spotvac_playlist_list


def upload_songs(final,spotvac_playlist_list):
    print('Now populating playlits')
    final = final
    spotvac_playlist_list = spotvac_playlist_list
    i = 0
    for entry in range(len(final)):
        stress = final['stress'][i]
        
        if stress < 0.2:
            #depression
            spt.user_playlist_add_tracks(user=username,playlist_id=spotvac_playlist_list['playlist_id'][0],tracks=[final['ids'][i]])
            print(f"Song {final['name'][i]} added to the playlist {spotvac_playlist_list['name'][0]}!")
            i+=1
        elif 0.2<=stress<0.4:
            #sad
            spt.user_playlist_add_tracks(user=username,playlist_id=spotvac_playlist_list['playlist_id'][1],tracks=[final['ids'][i]])
            print(f"Song {final['name'][i]} added to the playlist {spotvac_playlist_list['name'][1]}!")
            i+=1
        elif 0.4<=stress<0.6:
            #chill vibes
            spt.user_playlist_add_tracks(user=username,playlist_id=spotvac_playlist_list['playlist_id'][2],tracks=[final['ids'][i]])
            print(f"Song {final['name'][i]} added to the playlist {spotvac_playlist_list['name'][2]}!")
            i+=1
        elif 0.6<=stress<0.8:
            #good vibes
            spt.user_playlist_add_tracks(user=username,playlist_id=spotvac_playlist_list['playlist_id'][3],tracks=[final['ids'][i]])
            print(f"Song {final['name'][i]} added to the playlist {spotvac_playlist_list['name'][3]}!")
            i+=1
        elif 0.8<=stress<1.1:
            #happy
            spt.user_playlist_add_tracks(user=username,playlist_id=spotvac_playlist_list['playlist_id'][4],tracks=[final['ids'][i]])
            print(f"Song {final['name'][i]} added to the playlist {spotvac_playlist_list['name'][4]}!")
            i+=1
        else:
            pass

