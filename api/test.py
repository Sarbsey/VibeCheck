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
import faunadatafunctions as fdb
import pandas as pd
import time
import random
import json

username = '22mdb5fhocl2fobpsjbxvvkra'
client_id = os.environ['client_ID']
client_secret = os.environ['client_secret']
manager = SpotifyClientCredentials(client_id,client_secret)
token = 6
sp = spotipy.Spotify(client_credentials_manager=manager, auth=token)

full_user_info = {
    'data':{
        'user_id': '22mdb5fhocl2fobpsjbxvvkra'
    }
}
final = {
    'energy':[3,4,7,4,2,2,4,5,2,7,8,9,2,7,6,5,3,32]
}


lap = '4oA5fkQGa2rI7tmGJGT7GT'
track = '6ECp64rv50XVz93WvxXMGF'

g = fdb.length()
print(g)