import sqlite3

def get_piatti():
    query = 'SELECT * FROM piatti'
    connection = sqlite3.connect('db/mangiato.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query)

    result = cursor.fetchall()
    print(result)

    cursor.close()
    connection.close()

    return result

def get_piatto(id_piatto):
    query = 'SELECT * FROM piatti WHERE id = ?'

    connection = sqlite3.connect('db/mangiato.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query, (id_piatto,))

    result = cursor.fetchone()
    
    cursor.close()
    connection.close()

    return result

def get_recensioni(id_piatto):
    query = 'SELECT * FROM recensioni WHERE piatto = ?'

    connection = sqlite3.connect('db/mangiato.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(query, (id_piatto,))

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result

def add_recensione(recensione):
    query = 'INSERT INTO recensioni(testo_recensione,url_foto,valutazione,piatto) VALUES (?,?,?,?)'

    connection = sqlite3.connect('db/mangiato.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    success = False

    try:
        cursor.execute(query, (recensione['testo_recensione'],recensione['url_foto'],recensione['valutazione'], recensione['piatto']))
        connection.commit()
        success = True
    except Exception as e:
        print('Error', str(e))
        connection.rollback()

    cursor.close()
    connection.close()

    return success