from flask import Flask, request, render_template, redirect, session
from flask_session import Session
import spotipy
from spotipy import SpotifyClientCredentials
import os
import pandas as pd
from dotenv import load_dotenv
from urllib.parse import urlencode
from util import button
from util import faunadatafunctions as fdb
from util import Spotvac_functions as sf



app = Flask(__name__)
app.config['SESSION PERMANENT'] = False
secret_key = os.urandom(12).hex()
app.config['SECREY_KEY'] = secret_key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)



@app.route("/", methods=['GET','POST'])
def index():
  return render_template("index.html")

stateKey = 'spotify_auth_state'




@app.route("/launch_spotvac", methods=['GET','POST'])
def launch_spotvac():
  if request.method == "POST":

    full_auth_url = sf.request_authorization()
    
    return redirect(full_auth_url, code=302)
  

  elif request.method == "GET":
    '''
    Run SpotVac
    '''
    full_user_info = session.get('full_user_info', None)
    sp = session.get('spotipy_request', None)
    print('now running spotvac')
    sf.run_spotvac(sp, full_user_info)

    return redirect("/", code=302)




@app.route("/callback", methods=['GET','POST'])
def callback():
  token_data = sf.generate_token()
  user_info = sf.generate_user_info(token_data)
  submit = fdb.format_data(user_info, token_data)
  fdb.submit(submit)
  print('data submitted to fdb')


  client_id = os.environ['client_ID']
  client_secret = os.environ['client_secret']
  manager = SpotifyClientCredentials(client_id,client_secret)
  sp = spotipy.Spotify(client_credentials_manager=manager, auth=token_data['access_token'])


  session['spotipy_request'] = sp
  session['full_user_info'] = submit
  print('redirecting to launch spotvac')
  return redirect("/launch_spotvac", code=302)



@app.route("/counter_update")
def counter_update():
  num_list = fdb.length()
  return str(num_list)


@app.route("/documentation")
def documentation():
  return render_template('construction.html')

@app.route("/contact")
def contact():
  return render_template('construction.html')

@app.route("/other-links")
def other_links():
  return render_template('construction.html')

@app.route("/log")
def dev_log():
  return render_template('construction.html')



if __name__ == '__main__':
    app.run(port="5000", debug=True)

''''''
