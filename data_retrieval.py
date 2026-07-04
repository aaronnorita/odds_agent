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
        insert_odds_data(data_response)
        return data_response
        
    except requests.exceptions.RequestException:
        print(f"Failed to connect to the ODDs API")
        return None
    except (ValueError, KeyError):
        print(f"No odds found for this request")
        return None


def insert_odds_data(data_response):
    db_conn = sqlite3.connect("odds_data.db")
    cursor = db_conn.cursor()
    for game in data_response:
        cursor.execute("""
        INSERT INTO games (
            odds_api_event_id,
            sport,
            league,
            home_team,
            away_team,
            commence_time,
            home_score,
            away_score,
            status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (game["id"], game["sport_key"], game["sport_title"], game["home_team"], game["away_team"], game["commence_time"], None, None, "scheduled"))
        game_id = cursor.lastrowid
        for bookmaker in game["bookmakers"]:
            cursor.execute("""
            INSERT INTO bookmakers (
            odds_api_key,
            name,
            region
            ) VALUES (?, ?, ?)
            """, (bookmaker["key"], bookmaker["title"], "us"))
            bookmaker_id = cursor.lastrowid
            for market in bookmaker["markets"]:
                cursor.execute("""
                INSERT INTO odds_snapshots (
                    market_type,
                    spread_line,
                    home_price,
                    away_price,
                    fetched_at,
                    game_id,
                    bookmaker_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (market["key"], None, market["outcomes"][0]["price"],market["outcomes"][1]["price"], market["last_update"], game_id, bookmaker_id))
    db_conn.commit()
    db_conn.close()            
    
    
