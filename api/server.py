from flask import Flask, request, render_template

app = Flask(__name__)


# @ signifies a decorator - a way to wrap a function and modifying its behavior

@app.route("/", methods=['GET','POST'])
def index():
  return render_template("index.html")




@app.route("/launch_spotvac", methods=['GET','POST'])
def launch_spotvac():
  if request.method == "POST":
    # user_url = request.form['url-input']
    # button.test(user_url)
    return ('', 200)

'''
@app.route("/counter_update")
def counter_update():
  num_list = button.counter_update()
  return str(num_list)


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
