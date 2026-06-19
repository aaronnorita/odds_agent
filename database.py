import sqlite3

db_conn = sqlite3.connect("odds_data.db")
cursor = db_conn.cursor()