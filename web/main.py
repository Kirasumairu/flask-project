from flask import Flask, render_template

# filters: safe capitalize upper lower title trim striptags

app = Flask(__name__)

#@app.route('/')
#def index():
#  return "<h1>Hello World!</h1>"

@app.route('/')
def index():
  first_name = 'Johnny'
  code = '<strong>This is bolded</strong>'
  favorite_pizza = ['Pineapple', 'Margarita']
  return render_template(
    'index.html',
    first_name=first_name,
    code=code,
    favorite_pizza=favorite_pizza
  )

@app.route('/user/<name>')
def name(name):
  return render_template('user.html', user_name=name)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
  return render_template('500.html'), 500
