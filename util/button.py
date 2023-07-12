import spotipy
import os
import time
import sys
import pandas as pd
from spotipy import SpotifyClientCredentials, util, SpotifyOAuth, SpotifyException
from dotenv import load_dotenv

# Creates a playlist for a user

import argparse
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import faunadatafunctions as fdb




def run_spotvac(user_url):
    
    sp = spotipy_generate_token(user_url)
    user_info = sp.me()
    data_submit = fdb.format_data(user_info)
    fdb.submit(data_submit)
    
    db_length = fdb.length()

    return db_length


def verify(user_url):
    user_id = user_url.split("/")[-1]

    user_verification_data = fdb.look_up(user_id)
    return


def test(token_data):
    authorize_url = os.environ['authorize_url']
    client_id = os.environ['client_ID']
    client_secret = os.environ['client_secret']
    redirect_uri = os.environ['redirect_url']
    scope = 'playlist-modify-public'

    manager = SpotifyClientCredentials(client_id,client_secret)
    sp = spotipy.Spotify(client_credentials_manager=manager, auth=token_data['access_token'])

    print(sp.me())
    return





def counter_update():
    db_length = fdb.length()

    return db_length



def spotipy_generate_token(user_url):
    load_dotenv()
    api_base = os.environ['api_base']
    client_id = os.environ['client_ID']
    client_secret = os.environ['client_secret']
    redirect_uri = os.environ['redirect_url']
    username = user_url
    scope = 'playlist-modify-public'
    manager='penis'
    #sp = spotipy.Spotify(client_credentials_manager=manager, auth=token)
    return 




