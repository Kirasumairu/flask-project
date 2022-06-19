from flask import Flask, render_template

app = Flask(__name__)

#@app.route('/')
#def index():
#  return "<h1>Hello World!</h1>"

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/user/<name>')
def name(name):
  return "<h1>Hello {}</h1>".format(name)
