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

token = "BQAMAZk7XI78gQUmLuj8Z1vvvyJ0CpKrbAxcE9uB7AsjFilg6JiRIjz8O8dIDRd3WJOoVfxIlHiA6T3ip94ZREZpzfn0CUBnkDvIU0oVgmpTSxEhNA-_TOAbqTC92sGw7xP0nRUXPbIt6V6b4sKK-2l4Fdi3V5Wutoj5_xq5_jBNO109mwAoYD2q5hcAYFqxZ1CO6IxgpSqV3kLnfASjXlCNZ-62-jf5FZvIHw0zIhYHdM_LvJ9e4Q"
client_id = os.environ['client_ID']
client_secret = os.environ['client_secret']
manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=manager, auth=token)

g = sp.current_user_top_tracks(time_range='long_term')
bruh = []
for i in range(20):
    bruh.append(g['items'][i]['name'])
print(bruh)