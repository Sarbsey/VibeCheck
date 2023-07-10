from flask import Flask, request, render_template, redirect, session
from flask_session import Session

import spotipy
import spotipy.util as util
import os
from dotenv import load_dotenv
from util import button



app = Flask(__name__)


app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'

Session(app)


# @ signifies a decorator - a way to wrap a function and modifying its behavior

@app.route("/", methods=['GET','POST'])
def index():
  load_dotenv()
  api_base = os.environ['api_base']
  client_id = os.environ['client_ID']
  client_secret = os.environ['client_secret']
  redirect_uri = os.environ['redirect_url']
  cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
  auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private',
                                               cache_handler=cache_handler,
                                               redirect_uri=redirect_uri,
                                               client_id=client_id,
                                               client_secret=client_secret,
                                               show_dialog=True)
  if request.args.get("code"):
    # Step 2. Being redirected from Spotify auth page
    auth_manager.get_access_token(request.args.get("code"))
    return redirect('/')

  if not auth_manager.validate_token(cache_handler.get_cached_token()):
      # Step 1. Display sign in link when no token
      auth_url = auth_manager.get_authorize_url()
      return f'<h2><a href="{auth_url}">Sign in</a></h2>'

  # Step 3. Signed in, display data
  spotify = spotipy.Spotify(auth_manager=auth_manager)
  return f'<h2>Hi {spotify.me()["display_name"]}, ' \
          f'<small><a href="/sign_out">[sign out]<a/></small></h2>' \
          f'<a href="/playlists">my playlists</a> | ' \
          f'<a href="/currently_playing">currently playing</a> | ' \
      f'<a href="/current_user">me</a>' \
  #return render_template("index.html")




@app.route("/launch_spotvac", methods=['GET','POST'])
def launch_spotvac():
  if request.method == "POST":
    user_url = request.form['url-input']
    button.test(user_url)
    return redirect("/", code=302)
  if request.method == "GET":
    return redirect("/", code=302)






@app.route("/counter_update")
def counter_update():
  num_list = button.counter_update()
  return str(num_list)





'''
if __name__ == '__main__':
    app.run(port="8000", debug=True)

#finish later
@app.route("/test")
def test():
  return render_template('test.html')


@app.route("/documentation")
def documentation():
  return render_template('construction.html')

@app.route("/contact")
def contact():
  return render_template('construction.html')

@app.route("/other-links")
def other_links():
  return render_template('construction.html')

@app.route('/profile/<name>')
def profile(name):
  return render_template('profile.html', name=name)



if __name__ == '__main__':
    app.run(port="5000", debug=True)


@app.route('/')
def index():
  return "Method used: %s" % request.method

@app.route('/bacon', methods=['GET','POST'])
def bacon():
  if request.method == 'POST':
    return "You are using POST"
  else:
    return "I hate you"

@app.route('/tuna')
def tuna():
  return '<h2>Tuna is good</h2>'
  
@app.route('/profile/<username>')
def profile(username):
  return 'Ball Fart on %s' % username

@app.route('/post/<int:post_id>')
def post(post_id):
  return 'Ball Fart on %s' % post_id

@app.route('/')
def index():
  return render_template('index.html')
'''
