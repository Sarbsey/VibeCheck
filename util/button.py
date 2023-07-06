import spotipy
import os
import time
import sys
import pandas as pd
from IPython.display import clear_output
from spotipy import SpotifyClientCredentials, util, SpotifyOAuth, SpotifyException
from dotenv import load_dotenv

# Creates a playlist for a user

import argparse
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth






def test(user_url):              
    client_id = os.environ['client_ID']
    client_secret = os.environ['client_secret']
    redirect_uri = os.environ['redirect_url']
    username = user_url
    scope = 'playlist-modify-public'

    manager = SpotifyClientCredentials(client_id,client_secret)

    token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri) 
    sp = spotipy.Spotify(client_credentials_manager=manager, auth=token)
    user_info = sp.me()
    user_record = user_info['id']
    fp = open(r"./spotvac_users.txt", 'a+')
    fp.write('\n'+user_record)
    fr = open(r"./spotvac_users.txt", 'r')
    num_lines = len(fr.readlines())
    

    return num_lines

def counter_update():
    fr = open(r"./spotvac_users.txt", 'r')
    num_lines = len(fr.readlines())
    num_lines = '{:,}'.format(num_lines)
    return num_lines

