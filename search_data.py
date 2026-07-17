import datetime
import sqlite3


def get_todays_games(sport):
    """
    
    Fetches games for a given sport and todays date from the database.
    The parameter "sport" is a string that details exactly what sport to grab from the database.
    An example of this is 'americanfootball_ncaaf'.
    The function returns a list of games for todays date for a given sport.
    
    """
    
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
    """  
    
    Fetches odds for a given game (using the game_id, which is an int) from the database.
    This returns a list of dictionaries. Each dictionary has the bookmaker name, home price, and away price.
    
    """
    
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
    
    """
    
    Fetches the games for a given sport and the odds by each bookmaker
    This returns a dictionary of lists for games. The key value pair for this dictionary is the game_id (int) and the list for that game.
    In each list, there is a dictionary with the following key value pairs: bookmaker name, home & away price.

    """
    
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
    sports_odds = {}
    for game in all_sport_odds:
        if game['game_id'] not in sports_odds:
            sports_odds[game['game_id']] = []
        sports_odds[game['game_id']].append({"name": game['name'], "home_price": game['home_price'], "away_price": game['away_price']})
    
    return sports_odds
    

def get_line_movement(game_id, market_type):
    """
    
    Fetches the line movement per a given game and market type. 
    Inputs are a game_id and a market_type. This can be moneyline, spreads, etc.
    This returns a dictionary of lists with dictionaries inside them. The first dict has a bookmaker as the key and the list as the value.
    The keys and values are the market type (moneyline, spreads, etc.), home and away prices, and when these were recorded.
    
    """
    
    
    db_conn = sqlite3.connect("odds_data.db")
    db_conn.row_factory = sqlite3.Row
    cursor = db_conn.cursor()
    cursor.execute(""" 
        SELECT odds_snapshots.market_type, bookmakers.name, odds_snapshots.home_price, odds_snapshots.away_price, odds_snapshots.fetched_at
        FROM odds_snapshots
        INNER JOIN bookmakers ON bookmakers.id=odds_snapshots.bookmaker_id
        WHERE odds_snapshots.game_id = ? AND odds_snapshots.market_type = ?         
        ORDER BY odds_snapshots.fetched_at ASC;           
                   """,
                   (game_id, market_type))
    line_cols = cursor.fetchall()
    all_line_moves = [dict(row) for row in line_cols]
    db_conn.close()
    line_moves = {}
    for game in all_line_moves:
        if game['name'] not in line_moves:
            line_moves[game['name']] = []
        line_moves[game['name']].append({"market_type": game['market_type'], "home_price": game['home_price'], "away_price": game['away_price'], "fetched_at": game['fetched_at']})
    return line_moves