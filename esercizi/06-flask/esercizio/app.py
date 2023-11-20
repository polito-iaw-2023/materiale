# import module
from flask import Flask, render_template

# create the application
app = Flask(__name__)

menu = [
  {'type': 'Primi', 'plates': [{'name': 'pasta al tonno', 'promotion': True}, {'name': 'pasta al sugo'}]},
  {'type': 'Secondi', 'plates': [{'name': 'tonno', 'promotion': True}, {'name': 'cotoletta'}]},
  {'type': 'Contorni', 'plates': [{'name': 'fagiolini'}, {'name': 'patate al forno'}]},
  ]

# define the homepage
@app.route('/')
def index():
  return render_template('index.html', menu=menu)

# define the about page
@app.route('/about')
def about():
  return render_template('about.html')

# define the page of each first plates
@app.route('/first/<int:id>')
def first_plate(id): # indice del piatto nell'array "plates"
  plate = menu[0]['plates'][id-1]
  return render_template('single.html', plate=plate)
