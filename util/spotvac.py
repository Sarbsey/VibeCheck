#from Spotvac_functions import *
import spotipy
from spotipy import SpotifyClientCredentials, util
import numpy as np
import os
#from tensorflow import keras
from dotenv import load_dotenv
load_dotenv()

# Load HSM
#model = keras.models.load_model('./HSM')


client_id = os.environ['client_ID']
client_secret = os.environ['client_secret']
redirect_uri = os.environ['redirect_url']
username = 'https://open.spotify.com/user/31abdiahava3r7d5jg5hzzueeaoq' 
# os.environ['username']
scope = 'playlist-modify-public'
#print(redirect_uri)
manager = SpotifyClientCredentials(client_id,client_secret)
token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
sp = spotipy.Spotify(client_credentials_manager=manager, auth=token)
me = sp.me()
print(me['id'])


'''
I want to resolve this process down to these steps:

I. Collect the songs
    A. Determine from which playlists songs will be collected from
    B. Make a request (preferrably using the max amount of songs per request) to collect the song data
    C. Compile everything into one csv
II. Sort songs into the 11 different food groups
- note to self: this is based on Thayer's method of emotional classification
- other note to self: these categories are not numerically defined, need to determine it by my best estimates
    A. Need to figure out if 11 groups is too much
        i. can just have user input
        ii. maybe a small sort into 5 groups based on the corners
    B. Sort them intelligntly 
        i. I don't know how to do this
II. Produce the playlists
    A. This part honestly has no issues other than its slow






#I (need to add part A)


# Get important user data
#print("Now importing song data:")
plylst = download_user_playlists(username)
plylst = plylst.reset_index(drop=True)
# Somehow make an output so the user can select/deselect these (could just save it for an advanced version later)
id_playlist = plylst['playlist_id']


i = 0
psongs_list = pd.DataFrame()
for entry in id_playlist:
    name = plylst['name'][i]
    print(f"Now downloading songs from: {name}")
    playlist_songs = download_playlist(entry, 500)
    psongs_list = pd.concat([psongs_list, playlist_songs])
    i += 1
#print(psongs_list)    

#print("Prepping song data")
lsongs_list = download_liked_songs().drop_duplicates().reset_index(drop=True)
#print(lsongs_list)
dataset = pd.concat([lsongs_list,psongs_list]).drop_duplicates().reset_index(drop=True)
#dataset.to_csv('dataset')
#print(dataset)

i = 0
print('Now obtaining song features from spotify (this may take a while)')
preprocessed_dataset = pd.DataFrame()
for entry in range(len(dataset)):
    ids = dataset['song_id'][i]
    preprocessed_data = get_songs_features(ids)
    #print(preprocessed_data)
    preprocessed_dataset = pd.concat([preprocessed_data, preprocessed_dataset.loc[:]]).reset_index(drop=True)
    #print(preprocessed_dataset)
    i += 1
#print(preprocessed_dataset)
preprocessed_dataset.to_csv('prep.csv', index=False)


spotvac_playlist_list = create_spotipy_playlists()
final = evaluate_mood(preprocessed_dataset)
final = evaluate_energy(preprocessed_dataset)
#results = pd.concat([results, lsongs_list.loc[2]]).reset_index(drop=True)
final.to_csv('final.csv', index=False)
#print(results)


#final = pd.read_csv('final.csv')



upload_songs(final,spotvac_playlist_list)

print('-----------------------------------------------------------------------------------------')
print('\n')
print("All done, enjoy the playlists!")
'''