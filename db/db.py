import sqlite3


# to get if exist or create db
def is_exist_db():
    conn = sqlite3.connect('dnschanger.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            primary TEXT NOT NULL,
            secondary TEXT NULL,
        )
    ''')

    conn.commit()


# to add a row to table. get a dictionary with keys : 'name','primary','secondary'
def add_row(conn,values):
    # to add a row to table
    conn.cursor.execute(f'''
            INSERT INTO dns (name, primary, secondary) 
            VALUES ('{values['name']}', '{values['primary']}', '{values['secondary']}')
            ''')
    
    conn.commit()

# to edit a row
def edit_row(conn,dns):
    conn.cursor.execute(f'''
            UPDATE dns 
            SET name = '{dns['name']}' ,primary = '{dns['primary']}',secondary = '{dns['secondary']}'
            WHERE id = {dns['id']}
            ''')

    conn.commit()


# to delete a row
def delete_row(conn,id):
    conn.cursor.execute(f'DELETE FROM dns WHERE id = {id}')

    conn.commit()


# to get row or rows depend on pass id. must to pass a connection
def get(conn,id=None,):
    if id == None:
        conn.cursor.execute('SELECT * FROM dns')
        all_users = conn.cursor.fetchall()
        return all_users
    else:
        user = conn.cursor.execute(f'SELECT * FROM dns WHERE id = {id}')
        return user

