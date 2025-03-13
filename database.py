import sqlite3

DATABASE = 'sites.db'

# Функция для создания таблицы в базе данных
def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            xpath TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Функция для добавления данных в базу данных
def insert_data(title, url, xpath):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sites (title, url, xpath) VALUES (?, ?, ?)', (title, url, xpath))
    conn.commit()
    conn.close()