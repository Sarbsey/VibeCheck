import spotipy
import os
from spotipy import SpotifyClientCredentials, util, SpotifyOAuth, SpotifyException
from dotenv import load_dotenv
load_dotenv()

client_id = os.environ['client_ID']
client_secret = os.environ['client_secret']
redirect_uri = os.environ['redirect_url']
user_url = 'https://open.spotify.com/user/22mdb5fhocl2fobpsjbxvvkra'
scope = 'playlist-modify-public'

def spotipy_generate_token(user_url):
    load_dotenv()
    client_id = os.environ['client_ID']
    client_secret = os.environ['client_secret']
    redirect_uri = os.environ['redirect_url']
    username = user_url
    scope = 'playlist-modify-public'

    manager = SpotifyClientCredentials(client_id,client_secret)

    token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri) 
    sp = spotipy.Spotify(client_credentials_manager=manager, auth=token)
    return sp


sp = spotipy_generate_token(user_url)
user_info = sp.me()

print(user_info)