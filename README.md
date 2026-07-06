# odds_agent

A Python CLI sports betting odds agent powered by LangChain and The Odds API. Ask questions in natural language and get real-time odds comparisons, line movements, and game data stored locally in SQLite.

**Status:** In active development

## Setup

1. Clone the repo and create a virtual environment:
```bash
   python -m venv venv
   source venv/bin/activate
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```
   ODDS_API_KEY=your_odds_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

4. Run the agent:
```bash
   python main.py
```

## Usage

Type natural language queries at the prompt:

```
> What are today's NBA games?
> Compare moneyline odds for game 42 across all books
> Show me line movement for the Lakers game
> Fetch the latest NFL odds
```

Type `exit` or `quit` to stop.

## Project Structure

```
odds_agent/
├── database.py        # SQLite schema creation — COMPLETE
├── data_retrieval.py  # Fetches odds from The Odds API, inserts into SQLite — COMPLETE
├── search_data.py     # Query functions against the database — IN PROGRESS
├── agents.py          # LangChain agent with registered tools — IN PROGRESS
└── main.py            # Entry point and CLI loop — NOT STARTED
```

## Database Schema

- **games** — event metadata (teams, sport, status, scores)
- **bookmakers** — sportsbook registry
- **odds_snapshots** — timestamped odds per game per bookmaker

## Agent Tools

- `fetch_odds(sport, date)` — hits The Odds API and inserts results into SQLite. Registered.
- `get_todays_games(sport)` — planned
- `get_odds_for_game(game_id)` — planned
- `compare_books_for_sport(sport)` — planned
- `get_line_movement(game_id)` — planned

## API Keys

- The Odds API: [the-odds-api.com](https://the-odds-api.com)
- Anthropic API: [console.anthropic.com](https://console.anthropic.com)