from dotenv import load_dotenv
import requests
import os
import sqlite3

load_dotenv()

def fetch_odds(sport, date):
    """_summary_

    Args:
        sport (_type_): _description_
        date (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        api_key = os.getenv("THE_ODDS_API_KEY")
        params = {"apiKey": api_key, 
                "regions": "us",
                "markets": "h2h, spreads"}
        api_endpoint = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
        response = requests.get(api_endpoint, params=params)
        response.raise_for_status()
        data_response = response.json()
        
    except requests.exceptions.RequestException:
        print(f"Failed to connect to the ODDs API")
        return None
    except (ValueError, KeyError):
        print(f"No odds found for this request")
        return None
    
    
    db_conn = sqlite3.connect("odds_data.db")
    cursor = db_conn.cursor()
    cursor.execute("""
    INSERT INTO games (
        commence_time,
        home_team ,
        away_team,
        home_score,
        away_score,
        odds_api_event_id,
        sport,
        league,
        status      
    )
    VALUES ()
              """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookmakers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        odds_api_key TEXT NOT NULL,
        name TEXT NOT NULL,
        region TEXT NOT NULL      
    )
              """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS odds_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        market_type TEXT NOT NULL,
        spread_line REAL NOT NULL,
        home_price REAL NOT NULL,
        away_price REAL NOT NULL,
        fetched_at TEXT NOT NULL,
        game_id INTEGER NOT NULL,
        bookmaker_id INTEGER NOT NULL,
        FOREIGN KEY (game_id) REFERENCES games(id),
        FOREIGN KEY (bookmaker_id) REFERENCES bookmakers(id)
    )
              """)
    db_conn.commit()
    db_conn.close()"""