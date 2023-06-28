import sqlite3

API_TOKEN = 'your_token'
ID_CHANNEL = 'your_id_channel'


# connect DB
con = sqlite3.connect("channel_cars.db")
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS cars(
    state_number TEXT,
    photo TEXT,

    price INTEGER,
    brand TEXT,
    url_auto_ria TEXT,
    race TEXT,
    location TEXT
)""")