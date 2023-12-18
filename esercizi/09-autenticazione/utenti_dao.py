import sqlite3

def get_user_by_id(id_utente):
    query = 'SELECT * FROM utenti WHERE id = ?'

    connection = sqlite3.connect('db/mangiato.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query, (id_utente,))

    result = cursor.fetchone()
    
    cursor.close()
    connection.close()

    return result

def get_user_by_email(email_utente):

    query = 'SELECT * FROM utenti WHERE email = ?'

    connection = sqlite3.connect('db/mangiato.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query, (email_utente,))

    result = cursor.fetchone()
    
    cursor.close()
    connection.close()

    return result


def creare_utente(nuovo_utente):
    query = 'INSERT INTO utenti(nome,cognome,email,password) VALUES (?,?,?,?)'

    connection = sqlite3.connect('db/mangiato.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    success = False

    try:
        cursor.execute(query, (nuovo_utente['nome'],nuovo_utente['cognome'],nuovo_utente['email'], nuovo_utente['password']))
        connection.commit()
        success = True
    except Exception as e:
        print('Error', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success