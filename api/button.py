import spotipy
import os
import time
import sys
import pandas as pd
from flask_restful import Resource, Api, reqparse
from IPython.display import clear_output
from spotipy import SpotifyClientCredentials, util, SpotifyOAuth, SpotifyException
from dotenv import load_dotenv

# Creates a playlist for a user

import argparse
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger('examples.create_playlist')
logging.basicConfig(level='DEBUG')






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
    fp = open(r"spotvac_users.txt", 'a+')
    fp.write('\n'+user_record)
    fr = open(r"spotvac_users.txt", 'r')
    num_lines = len(fr.readlines())
    

    return num_lines

def counter_update():
    fr = open(r"spotvac_users.txt", 'r')
    num_lines = len(fr.readlines())
    num_lines = '{:,}'.format(num_lines)
    return num_lines


def get_args():
    parser = reqparse.RequestParser()
    parser.add_argument('p', required=True)
    parser.add_argument('d', required=False)
    args = parser.parse_args()
    return args

def auth():
    load_dotenv()
    client_id = os.environ['client_ID']
    client_secret = os.environ['client_secret']
    redirect_uri = os.environ['redirect_url']
    username = os.environ['username']
    scope = "playlist-modify-public"
    token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri) 
    manager = SpotifyClientCredentials(client_id,client_secret)
    return manager,token


def main():
    args = get_args()
    manager,token = auth()
    username = '22mdb5fhocl2fobpsjbxvvkra'
    sp = spotipy.Spotify(client_credentials_manager=manager, auth=token)
    #user_id = sp.me()['id']
    spt = spotipy.Spotify(auth=token)
    print(args)
    #spt.user_playlist_create(user=username, name=args['p'], public=True, description=str(args['d']))
    return args


if __name__ == '__main__':
    main()