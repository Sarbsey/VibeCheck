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

authorize_url = os.environ['authorize_url']
client_id = os.environ['client_ID']
client_secret = os.environ['client_secret']
redirect_uri = os.environ['redirect_url']
scope = 'playlist-modify-public'


token = {'access_token': 'BQAtnBY8lZihu6Q7DEk9DIhM424eG9mQMJbgHrfCGtqiVYqVIOL5snRmdRmZGsKisHzyk-HWZZLOugNPZ-lyU-anpDKTxxbVn40j_qeO45UBg8JMoxscFIOpmvfqtvhIREM_JcFU7VuRE-ZAHVXRypzM5zq0epZZnDi4HwdmUm-U0d_xCCwemQy-nDWSHph0SlrPmPAZzjXWF6P6bOeqUTEwM0PCmhEgtqvk4Q', 'token_type': 'Bearer', 'expires_in': 3600, 'refresh_token': 'AQDmOVCBZYn8KSEagkDnKmnf5OPvpB5yoMWghhiZCOiQmaf9xilqXs5FrNoJFDdu-ilqh4yGSEM5edYRovs0D1APx2lx3q3olWZlBKWQGx6wEEQJZNFiux7QGC7_lJH7NJ8', 'scope': 'playlist-modify-public'}
manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=manager, auth=token['access_token'])

print(sp.me())