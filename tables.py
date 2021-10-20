import sqlite3

con = sqlite3.connect('database')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS admins(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(60) NOT NULL,
    url VARCHAR(200) NOT NULL,
    username VARCHAR(100) NOT NULL,
    password VARCHAR NOT NULL
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    product_id INTEGER NOT NULL,
    scrap_url TEXT NOT NULL,
    xpath TEXT NOT NULL
)''')

con.commit()