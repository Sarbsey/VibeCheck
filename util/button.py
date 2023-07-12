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


'''
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
'''


