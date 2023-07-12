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
import testfauna as fdb
import Spotvac_functions as sf




def run_spotvac(user_url):
    # Step 0: Verify user details in database (can skip step 1 later)
    #fdb.verify(user_url) // This isn't actually written

    # Step 1: Generate a token for the user and submit data to fdb
    sp = sf.spotipy_generate_token(user_url)
    user_info = sp.me()
    data_submit = fdb.format_data(user_info)
    fdb.submit(data_submit)
    
    db_length = fdb.length()

    # Step 2: Pass everything to spotvac and generate the playlists

    
    return db_length


def verify(user_url):
    user_id = user_url.split("/")[-1]

    user_verification_data = fdb.look_up(user_id)
    return


def counter_update():
    db_length = fdb.length()

    return db_length
