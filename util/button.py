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


from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient




def test(user_url):
    
    sp = spotipy_generate_token(user_url)
    user_info = sp.me()
    data_submit = format_data(user_info)
    fauna_submit(data_submit)
    
    db_length = fauna_length()

    return db_length

def counter_update():
    db_length = fauna_length()

    return db_length

def spotipy_generate_token(user_url):
    load_dotenv()
    api_base = os.environ['api_base']
    client_id = os.environ['client_ID']
    client_secret = os.environ['client_secret']
    redirect_uri = os.environ['redirect_url']
    username = user_url
    scope = 'playlist-modify-public'

    sp = spotipy.Spotify(client_credentials_manager=manager, auth=token)
    return sp

def fauna_submit(data_submit):
    fc = FaunaClient(
    secret=os.environ['fauna_secret'],
    endpoint="https://db.fauna.com/"
    )
    doc_uid = fc.query(q.new_id())


    fc.query(
    q.create(
    q.ref(
    q.collection('spotvac_users'), doc_uid), data_submit
    ))
    return


def fauna_length():
    fc = FaunaClient(
    secret=os.environ['fauna_secret'],
    endpoint="https://db.fauna.com/"
    )

    length = fc.query(
    q.count(
    q.paginate(
    q.documents(
    q.collection('spotvac_users')))))

    db_length = length['data'][0]
    return db_length


def format_data(user_info):
    name = user_info['display_name']
    name = name.split()
    user_id = user_info['id']
    FirstName = name[0]
    LastName = name[1:]

    submit = {"data":{
    "user_id" : user_id,
    "user_data":{
        "FirstName":FirstName,
        "LastName":LastName
            }
        }
    }

    return submit