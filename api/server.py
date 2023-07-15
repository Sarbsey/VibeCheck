from flask import Flask, request, render_template, redirect, session
from flask_session import Session
import spotipy
import spotipy.util as util
import os
from dotenv import load_dotenv
import secrets
import string
import requests
from urllib.parse import urlencode
import base64
from util import button
from util import faunadatafunctions as fdb
from util import Spotvac_functions as sf


app = Flask(__name__)



@app.route("/", methods=['GET','POST'])
def index():
  return render_template("index.html")

stateKey = 'spotify_auth_state'

@app.route("/launch_spotvac", methods=['GET','POST'])
def launch_spotvac():
  

  if request.method == "POST":
    user_url = request.form['url-input']
    if user_url:
      '''
      button.verify(user_url)
      button.run_spotvac(user_url)
      '''
      state = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(16))

      authorize_url = os.environ['authorize_url']
      client_id = os.environ['client_ID']
      client_secret = os.environ['client_secret']
      redirect_uri = os.environ['redirect_url']
      scope = 'playlist-modify-public'

      auth_dict = {
          'client_id': client_id,
          'response_type': 'code',
          'redirect_uri': redirect_uri,
          'scope': scope,
          'state': state
      }

      params = urlencode(auth_dict)
      full_auth_url = f"{authorize_url}" + params

    else:
      print('bruh')
    return redirect(full_auth_url, code=302)
  else:
    return redirect("/", code=302)


@app.route("/callback", methods=['GET','POST'])
def callback():
  token_url = os.environ['token_url']
  client_id = os.environ['client_ID']
  client_secret = os.environ['client_secret']
  redirect_uri = os.environ['redirect_url']
  scope = 'playlist-modify-public'
  code = request.args.get('code')
  

  auth_header = base64.urlsafe_b64encode((client_id + ':' + client_secret).encode())
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic %s' % auth_header.decode('ascii')
  }

  data = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': redirect_uri
  }
  


  full_access_token = requests.post(url=token_url, data=data, headers=headers)
  token_data = full_access_token.json()
  user_info = sf.generate_token(token_data)
  submit = fdb.format_data(user_info, token_data)
  fdb.submit(submit)
  return redirect("/", code=302)



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
def other_links():
  return render_template('construction.html')


'''
if __name__ == '__main__':
    app.run(port="5000", debug=True)

'''
