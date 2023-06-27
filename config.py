import sqlite3

API_TOKEN = 'token_bot'
ID_CHANNEL = -1001802881394
TIMER = ''


# connect DB
con = sqlite3.connect("channel_cars.db")
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS cars(
    price INTEGER,
    state_number TEXT
)""")