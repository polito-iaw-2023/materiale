# import module
from flask import Flask, render_template, request, redirect, url_for
import piatti_dao

# create the application
app = Flask(__name__)

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
def signup():
    return render_template('signup.html')

@app.route('/recensioni/new', methods=['POST'])
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