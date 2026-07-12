import datetime
import sqlite3


def get_todays_games(sport):
    pre_string_date = datetime.date.today()
    date_str = str(pre_string_date)
    db_conn = sqlite3.connect("odds_data.db")
    db_conn.row_factory = sqlite3.Row
    cursor = db_conn.cursor()
    cursor.execute("""
        SELECT * 
        FROM games
        WHERE substr(commence_time, 1, 10) = ? AND sport = ?
        ORDER BY commence_time DESC;            
        """,  (date_str, sport))
    rows = cursor.fetchall()
    games = [dict(row) for row in rows]
    db_conn.close()
    return games

def get_odds_for_gamnes(games):
    db_conn = sqlite3.connect("odds_data.db")
    cursor = db_conn.cursor()
    cursor.execute(""" 
        FROM 
        JOIN ON            
                   """)