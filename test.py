import spotipy
import os
from spotipy import SpotifyClientCredentials, util, SpotifyOAuth, SpotifyException
from dotenv import load_dotenv
load_dotenv()
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import os
from urllib.request import urlretrieve
from urllib.parse import urlencode
import webbrowser
import requests
import secrets
import string
#import Spotvac_functions as sf
#import faunadatafunctions as fdb
import pandas as pd
import time
import random
import json

def submit(data_submit):
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

def format_data(user_info, token_data, sp):
    name = user_info['display_name']
    name = name.split()
    user_id = user_info['id']
    FirstName = name[0]
    LastName = name[1:]

    submit = {"data":{
    "user_id" : user_id,
    "user_data":{
        "FirstName":FirstName,
        "LastName":LastName,
            },
    "spotipy_data":{
        "token_data": token_data,
        "spotipy_authorization": sp
            },
        }
    }

    return submit

def look_up(user_id):
    fc = FaunaClient(
    secret=os.environ['fauna_secret'],
    endpoint="https://db.fauna.com/"
    )

    fdb_user_search = fc.query(
    q.paginate(q.match(
    q.index("test2"), user_id)) 
    )
    
    fdb_search_results = fdb_user_search['data']

    user_verification_data = fc.query(
        q.map_(
        q.lambda_("name", q.get(q.var("name"))),
        fdb_search_results
    ))

    return user_verification_data[-1]['data']

token_data = {
    'access_token' : 'penis' 
}
client_id = os.environ['client_ID']
client_secret = os.environ['client_secret']
manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=manager, auth=token_data['access_token'])

user_info = {'id': '22mdb5fhocl2fobpsjbxvvkra', 'display_name': 'Eric Sarbacker'}
             
#g = format_data(user_info, token_data, sp)
#submit(g)
print(sp)

#f = look_up('22mdb5fhocl2fobpsjbxvvkra')
#print(f[-1]['data'])