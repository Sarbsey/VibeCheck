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

def retrieve(ts):
    fc = FaunaClient(
    secret=os.environ['fauna_secret'],
    endpoint="https://db.fauna.com/"
    )
    

    g = fc.query(
    q.match(
    q.ref(
    q.collection('spotvac_users')),  ts
    ))
    return g


def look_up(ts):
    fc = FaunaClient(
    secret=os.environ['fauna_secret'],
    endpoint="https://db.fauna.com/"
    )

    fdb_user_search = fc.query(
    q.paginate(q.match(
    q.index("test2"), ts)) 
    )
    
    fdb_search_results = fdb_user_search['data']
    #print(f' search found {fdb_search_results}')
    user_verification_data = fc.query(
        q.map_(
        q.lambda_("ts", q.get(q.var("ts"))),
        fdb_search_results
    ))

    return user_verification_data


f = look_up('22mdb5fhocl2fobpsjbxvvkra')
print(f[-1]['data'])