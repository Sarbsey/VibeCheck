import spotipy
from spotipy import SpotifyClientCredentials, util, SpotifyOAuth
import os
import time
import sys
import time
import pandas as pd
from dotenv import load_dotenv
import numpy as np
from urllib.request import urlretrieve
from urllib.parse import urlencode
import secrets
import string
import requests
from flask import request
import base64


load_dotenv()

# Load HSM
#HSM_model = keras.models.load_model('./HSM')
#HEM_model = keras.models.load_model('./HEM')
#HEE_model = keras.models.load_model('./HEE')

#client_id = os.environ['client_ID']
#client_secret = os.environ['client_secret']
#redirect_uri = os.environ['redirect_url']
#username = os.environ['username']
#scope = 'playlist-modify-public user-library-read'



def request_authorization():
        
    '''
    user_url = request.form['url-input']
    button.verify(user_url)
    button.run_spotvac(user_url)
    '''
    state = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(16))

    authorize_url = os.environ['authorize_url']
    client_id = os.environ['client_ID']
    redirect_uri = os.environ['redirect_url']
    scope = 'playlist-modify-public user-library-read user-read-private'

    auth_dict = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope,
        'state': state
    }

    params = urlencode(auth_dict)
    full_auth_url = f"{authorize_url}" + params
    return full_auth_url


def generate_token():
    token_url = os.environ['token_url']
    client_id = os.environ['client_ID']
    client_secret = os.environ['client_secret']
    redirect_uri = os.environ['redirect_url']
    code = request.args.get('code')
    

    auth_header = base64.urlsafe_b64encode((client_id + ':' + client_secret).encode())
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic %s' % auth_header.decode('ascii')
    }

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }
    


    full_access_token = requests.post(url=token_url, data=data, headers=headers)
    token_data = full_access_token.json()
    return token_data


def generate_user_info(token_data):
    client_id = os.environ['client_ID']
    client_secret = os.environ['client_secret']


    manager = SpotifyClientCredentials(client_id,client_secret)
    sp = spotipy.Spotify(client_credentials_manager=manager, auth=token_data['access_token'])

    user_info = sp.me()
    return user_info


def run_spotvac(sp, full_user_info):


    #start = time.time()
    playlist_list = download_user_playlists(sp, full_user_info)
    #timer1 = time.time()
    #elapsed = timer1 - start
    #print(f'user playlists downloaded, time: {elapsed}')


    songs_list = pd.DataFrame()
    for playlist in playlist_list['playlist_id']:
      temp = download_playlist(sp, playlist)
      songs_list = pd.concat([songs_list, temp])
    

    #timer2 = time.time()
    #elapsed = timer2 - timer1
    #print(f'playlist tracks downloaded, time: {elapsed}')


    liked_songs = download_liked_songs(sp)
    #timer3 = time.time()
    #elapsed = timer3 - timer2
    #print(f'liked songs downloaded, time: {elapsed}')


    full_songs_list = pd.concat([songs_list, liked_songs])
    full_songs_list = full_songs_list.drop_duplicates()
    full_songs_dataset = download_song_data(sp, full_songs_list)

    full_songs_dataset = full_songs_dataset.reset_index().reset_index()
    full_songs_list = full_songs_list.reset_index().reset_index()

    #full_songs_list.to_csv('full_list2.csv')
    #full_songs_dataset.to_csv('full_data2.csv')
    final_dataset = pd.merge(full_songs_list, full_songs_dataset, on='level_0')
    #final_dataset.to_csv('final2.csv')
    #timer4 = time.time()
    #elapsed = timer4 - timer3
    #print(f'song features downloaded, time: {elapsed}')
    spotvac_playlist_list = create_spotipy_playlists(sp, full_user_info)
    #timer5 = time.time()
    #elapsed = timer5 - timer4
    #print(f'playlists created, time: {elapsed}')
    upload_songs(sp, full_user_info, final_dataset, spotvac_playlist_list)
    #timer6 = time.time()
    #elapsed = timer6 - timer5
    #print(f'songs uploaded, time: {elapsed}')

    return


def download_user_playlists(sp, full_user_info):
    username = full_user_info['data']['user_id']

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


def download_playlist(sp,id_playlist):
    songs_list = pd.DataFrame(columns=['song_id','name'])
    # Get the entire playlist
    page_of_songs = sp.playlist_tracks(id_playlist)
    data = [[]]

    while page_of_songs:
        # Get 100 songs from the playlist 
        for i,songs in enumerate(page_of_songs['items']):
            song_id = songs['track']['id']
            name = songs['track']['name']
            data = [[song_id, name]]
            temp = pd.DataFrame(data, columns=['song_id','name'])
            songs_list = pd.concat([songs_list, temp])

        # Go to next page of playlist
        if page_of_songs['next']:
            page_of_songs = sp.next(page_of_songs)

        # End if theres no more pages
        else:
            page_of_songs = None
    
    return songs_list


def download_liked_songs(sp):
    # print('Now downloading liked songs')
 
    results = sp.current_user_saved_tracks()
    songlist = pd.DataFrame()
    data = [[]] 

    while results:
        for i,result in enumerate(results):
            for item in results['items']:
                track = item['track']
                #print("%32.32s %s" % (track['artists'][0]['name'], track['name']))
                song_id = track['id']
                song_name = track['name']
                data = [[song_id, song_name]]
                time.sleep(0.05)
                temp = pd.DataFrame(data, columns=['song_id','name'])
                songlist = pd.concat([songlist, temp])
            if results['next']:
                results = sp.next(results)
            else:
                results = None
                break
    return songlist


'''
def get_playlist_tracks(sp,playlist_list):
    for i,id in enumerate(playlist_list['playlist_id']):
        playlist_id = id
        results = sp.user_playlist_tracks(username,playlist_id)
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
    return tracks
'''


def download_song_data(sp, full_songs_list):
    

    

    length = len(full_songs_list)
    #print(f'There are {length} songs in the full list')
    repeats = int(length / 50)
    remainder = length % 50
    #print(f'The finction should repeat {repeats+1} times with a final list of length {remainder}')

    full_song_dataset = pd.DataFrame()
    temp_list = []
    k = 0
    for i,song in enumerate(full_songs_list['song_id']):
        temp_list.append(song)
        if len(temp_list) == 50:
            n_songs = len(temp_list)
            temp = get_songs_features(sp, temp_list, n_songs)
            full_song_dataset = pd.concat([full_song_dataset, temp])
            #print(f'song data has been retrieved with a list of length {len(temp_list)}')
            temp_list = []
            k += 1
            


        elif k == repeats and len(temp_list) == remainder:
            n_songs = len(temp_list)
            temp = get_songs_features(sp, temp_list, n_songs)
            full_song_dataset = pd.concat([full_song_dataset, temp])
            #print(f'song data has been retrieved with a list of length {len(temp_list)}')
            temp_list = []
            k+=1
            #print(f'song data had its final retrieval with a total of {k} repeats')
    i+= 1
    return full_song_dataset


def get_songs_features(sp, songs, n_songs):
    # meta = sp.tracks(songs)
    features = sp.audio_features(songs)

    preprocessed_data = pd.DataFrame(columns = ['energy','valence'])
    i = 0
    for i in range(n_songs):
        # meta
        # name = meta['tracks'][i]['id']
        # ids =  meta['id']
        #features
        energy = features[i]['energy']
        valence = features[i]['valence']

        track = [[energy, valence]]
        temp = pd.DataFrame(track, columns = ['energy','valence'])
        preprocessed_data = pd.concat([preprocessed_data,temp])
    return preprocessed_data


def add_song_feature(sp, ids):

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


def create_spotipy_playlists(sp, full_user_info):
    username = full_user_info['data']['user_id']
    #print('Now creating playlists')
    sp.user_playlist_create(user=username, name='Spotvac: Angry', public=True, description='A playlist with Angry music')
    time.sleep(0.3)
    #print('Playlist Spotvac: Happy Created')
    sp.user_playlist_create(user=username, name='Spotvac: Happy', public=True, description='A playlist with Happy music')
    time.sleep(0.3)
    #print('Playlist Spotvac: Good Vibes Created')
    sp.user_playlist_create(user=username, name='Spotvac: Chill', public=True, description='A playlist with Chill music')
    time.sleep(0.3)
    #print('Playlist Spotvac: Chill Vibes Created')
    sp.user_playlist_create(user=username, name='Spotvac: Sad', public=True, description='A playlist with Sad music')
    time.sleep(0.3)
    #print('Playlist Spotvac: Sad Created')
    sp.user_playlist_create(user=username, name='Spotvac: Peaceful', public=True, description='A playlist with Peaceful music')
    time.sleep(0.3)
    #print('Playlist Spotvac: Depression Created')
    time.sleep(5)
    spotvac_playlist_list = download_user_playlists(sp, full_user_info)
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


def upload_songs(sp, full_user_info, final_dataset, spotvac_playlist_list):
    username = full_user_info['data']['user_id']
    final = final_dataset
    spotvac_playlist_list = spotvac_playlist_list
    i = 0
    for entry in range(len(final)):
        energy = final['energy'][i]
        valence = final['valence'][i]
        
        q = song_vibe_test(valence, energy)

        if not q == 5:
            sp.user_playlist_add_tracks(user=username,playlist_id=spotvac_playlist_list['playlist_id'][q],tracks=[final['song_id'][i]])
            #print(f"Song {final['name'][i]} added to the playlist {spotvac_playlist_list['name'][q]}!")
            i+=1
        else:
            i+=1
            pass


def song_vibe_test(valence, energy):
    pos_curve =  0.5 + (0.064 - (valence - 0.5)**2 )**0.5
    neg_curve =  0.5 - (0.064 - (valence - 0.5)**2 )**0.5

    is_outside = (valence < 0.248) | (valence > 0.752)
    if is_outside:
        if (energy >= 0.5) & (valence < 0.5):
            #angry
            return  4
        elif (energy >= 0.5) & (valence >= 0.5):
            # happy
            return 3
        elif (energy < 0.5) & (valence < 0.5):
            # sad
            return 1
        elif (energy < 0.5) & (valence >= 0.5):
            # peaceful
            return 0
    else:
        if (energy >= pos_curve) & (valence < 0.5):
            #angry
            return  4
        elif (energy >= pos_curve) & (valence >= 0.5):
            # happy
            return 3
        elif (energy < neg_curve) & (valence < 0.5):
            # sad
            return 1
        elif (energy < neg_curve) & (valence >= 0.5):
            # peaceful
            return 0
        else:
            return 2