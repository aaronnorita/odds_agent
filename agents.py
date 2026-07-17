from langchain.agents import create_agent
from data_retrieval import fetch_odds
from search_data import get_todays_games, get_odds_for_game, compare_books_for_sport, get_line_movement
from dotenv import load_dotenv

load_dotenv()

agent = create_agent(
    model="claude-sonnet-5",
    tools=[fetch_odds, get_todays_games, get_odds_for_game, compare_books_for_sport, get_line_movement],
    system_prompt="You are a sports betting analyst",
)