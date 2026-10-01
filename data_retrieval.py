from dotenv import load_dotenv
import requests
import os
import sqlite3

load_dotenv()

def fetch_odds(sport: str) -> list | None:
    """

    Fetches current odds for a given sport from The Odds API and inserts them into the database.
    The Odds API's /odds endpoint only returns current/upcoming games, so there is no date filter.

    """
    try:
        api_key = os.getenv("THE_ODDS_API_KEY")
        params = {"apiKey": api_key, 
                "regions": "us",
                "markets": "h2h,spreads"}
        api_endpoint = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
        response = requests.get(api_endpoint, params=params)
        response.raise_for_status()
        data_response = response.json()
        insert_odds_data(data_response)
        return data_response
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to the ODDs API {e}")
        return None
    except (ValueError, KeyError) as e:
        print(f"No odds found for this request {e}")
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
        ON CONFLICT(odds_api_event_id) DO UPDATE SET
            commence_time = excluded.commence_time,
            home_team = excluded.home_team,
            away_team = excluded.away_team
        """, (game["id"], game["sport_key"], game["sport_title"], game["home_team"], game["away_team"], game["commence_time"], None, None, "scheduled"))
        cursor.execute("SELECT id FROM games WHERE odds_api_event_id = ?", (game["id"],))
        game_id = cursor.fetchone()[0]
        for bookmaker in game["bookmakers"]:
            cursor.execute("""
            INSERT INTO bookmakers (
            odds_api_key,
            name,
            region
            ) VALUES (?, ?, ?)
            ON CONFLICT(odds_api_key) DO UPDATE SET
                name = excluded.name,
                region = excluded.region
            """, (bookmaker["key"], bookmaker["title"], "us"))
            cursor.execute("SELECT id FROM bookmakers WHERE odds_api_key = ?", (bookmaker["key"],))
            bookmaker_id = cursor.fetchone()[0]
            for market in bookmaker["markets"]:
                spread_line = market["outcomes"][0].get("point") if market["key"] == "spreads" else None
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
                """, (market["key"], spread_line, market["outcomes"][0]["price"],market["outcomes"][1]["price"], market["last_update"], game_id, bookmaker_id))
    db_conn.commit()
    db_conn.close()            
    
    
