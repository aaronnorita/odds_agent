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
        """,  
        (date_str, sport))
    rows = cursor.fetchall()
    games = [dict(row) for row in rows]
    db_conn.close()
    return games

def get_odds_for_game(game_id):
    db_conn = sqlite3.connect("odds_data.db")
    db_conn.row_factory = sqlite3.Row
    cursor = db_conn.cursor()
    cursor.execute(""" 
        SELECT bookmakers.name, odds_snapshots.home_price, odds_snapshots.away_price
        FROM odds_snapshots
        INNER JOIN bookmakers ON bookmakers.id=odds_snapshots.bookmaker_id
        WHERE odds_snapshots.game_id = ?;           
                   """,
                   (game_id,))
    game_cols = cursor.fetchall()
    game_odds = [dict(row) for row in game_cols]
    db_conn.close()
    return game_odds

def compare_books_for_sport(sport):
    db_conn = sqlite3.connect("odds_data.db")
    db_conn.row_factory = sqlite3.Row
    cursor = db_conn.cursor()
    cursor.execute(""" 
        SELECT odds_snapshots.game_id, bookmakers.name, odds_snapshots.home_price, odds_snapshots.away_price
        FROM odds_snapshots
        INNER JOIN bookmakers ON bookmakers.id=odds_snapshots.bookmaker_id
        INNER JOIN games ON games.id=odds_snapshots.game_id
        WHERE games.sport = ?;           
                   """,
                   (sport,))
    sport_cols = cursor.fetchall()
    all_sport_odds = [dict(row) for row in sport_cols]
    db_conn.close()
    sport_odds = {}
    for game in all_sport_odds:
        if game['game_id'] not in sport_odds:
            sport_odds[game['game_id']] = []
    
    
    return sport_odds
    

def get_line_movement(game_id):
    return None