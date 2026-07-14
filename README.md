# odds_agent

A Python CLI sports betting odds agent powered by LangChain and The Odds API. Ask questions in natural language and get real-time odds comparisons, line movements, and game data stored locally in SQLite.

**Status:** Personal learning project, in active development — not production software.

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
   THE_ODDS_API_KEY=your_odds_api_key_here
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
- `get_todays_games(sport)` — complete. Filters `games` by `sport` and today's date (via `substr(commence_time, 1, 10)`), returns a list of dicts.
- `get_odds_for_game(game_id)` — complete. Joins `odds_snapshots` with `bookmakers` to return human-readable bookmaker names alongside odds for a single game.
- `compare_books_for_sport(sport)` — in progress. Joins `odds_snapshots`, `bookmakers`, and `games` to compare odds across all bookmakers for every game in a sport, grouped by game.
- `get_line_movement(game_id)` — not started

## Roadmap

**v1 (current):** CLI agent that fetches odds from The Odds API, stores them in SQLite, and answers natural language queries through LangChain-registered tools.

**v2 (planned):** Odds calibration analysis. Convert stored prices (e.g. -150) into implied win probabilities, then compare against actual outcomes (`home_score` vs `away_score` in the `games` table) to measure how accurate the odds have historically been.

**v3 (planned):** Line movement prediction. Builds on v2's output rather than standing alone — line movement is only meaningful in light of how reliable the odds are as a signal in the first place. Calibration analysis has to come first to establish that baseline; without it, a "prediction" about line movement would be indistinguishable from noise.

**Future:** Kalshi integration — automated trading bot (order execution, portfolio/risk management). A meaningfully higher-stakes tier of the project, to be tackled once the odds/reasoning layer is solid.

## API Keys

- The Odds API: [the-odds-api.com](https://the-odds-api.com)
- Anthropic API: [console.anthropic.com](https://console.anthropic.com)