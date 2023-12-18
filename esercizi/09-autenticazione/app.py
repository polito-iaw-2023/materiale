# import module
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

import piatti_dao
import utenti_dao
from models import User

# create the application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'qualsiasi valore'

login_manager = LoginManager()
login_manager.init_app(app)

# define the homepage
@app.route('/')
def index():
  piatti_db = piatti_dao.get_piatti()
  return render_template('index.html', piatti=piatti_db)

@app.route('/piatti/<int:id>')
def piatto_singolo(id):
  piatto_db = piatti_dao.get_piatto(id)
  recensioni_db = piatti_dao.get_recensioni(id)
  return render_template('single.html', piatto = piatto_db, recensioni=recensioni_db)

# define the about page
@app.route('/about')
def about():
  return render_template('about.html')

# define the signup page
@app.route('/iscriviti')
def iscriviti():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():

  new_user_from_form = request.form.to_dict()

  print(new_user_from_form)

  if new_user_from_form ['nome'] == '':
    app.logger.error('Il campo non può essere vuoto')
    return redirect(url_for('index'))

  if new_user_from_form ['cognome'] == '':
    app.logger.error('Il campo non può essere vuoto')
    return redirect(url_for('index'))

  if new_user_from_form ['email'] == '':
    app.logger.error('Il campo non può essere vuoto')
    return redirect(url_for('index'))

  if new_user_from_form ['password'] == '':
    app.logger.error('Il campo non può essere vuoto')
    return redirect(url_for('index'))
  
  new_user_from_form ['password'] = generate_password_hash(new_user_from_form ['password'])

  success = utenti_dao.creare_utente(new_user_from_form)

  if success:
    return redirect(url_for('index'))

  return redirect(url_for('iscriviti'))

@app.route('/login', methods=['POST'])
def login():

  utente_form = request.form.to_dict()

  utente_db = utenti_dao.get_user_by_email(utente_form['email'])

  if not utente_db or not check_password_hash(utente_db['password'], utente_form['password']):
    flash("Non esiste l'utente")
    return redirect(url_for('index'))
  else:
    new = User(id=utente_db['id'], nome=utente_db['nome'], cognome=utente_db['cognome'], email=utente_db['email'], password=utente_db['password'] )
    login_user(new, True)
    flash('Success!')

    return redirect(url_for('index'))

@app.route('/recensioni/new', methods=['POST'])
@login_required
def add_recensione():

  recensione = request.form.to_dict()

  if recensione ['recensione'] == '':
    app.logger.error('Il campo non può essere vuoto')
    return redirect(url_for('index'))

  foto = request.files['imgRecensione']
  if foto.filename != '':
    foto.save('static/'+foto.filename)
    recensione['url_foto'] = foto.filename

  rec = {'testo_recensione': 'test', 'url_foto': 'test_url', 'valutazione': 4, 'piatto': 1}
  piatti_dao.add_recensione(rec)

  return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):

    db_user = utenti_dao.get_user_by_id(user_id)

    user = User(id=db_user['id'],	nome=db_user['nome'],	cognome=db_user['cognome'],	email=db_user['email'],	password=db_user['password'])

    return user

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
