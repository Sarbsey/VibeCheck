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

