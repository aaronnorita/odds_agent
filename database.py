import sqlite3


def create_table():
    db_conn = sqlite3.connect("odds_data.db")
    cursor = db_conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        commence_time TEXT NOT NULL,
        home_team TEXT NOT NULL,
        away_team TEXT NOT NULL,
        home_score INTEGER NOT NULL,
        away_score INTEGER NOT NULL,
        odds_api_event_id TEXT UNIQUE,
        sport TEXT NOT NULL,
        league TEXT NOT NULL,
        status TEXT NOT NULL      
    )
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
    db_conn.close()