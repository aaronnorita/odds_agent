from langchain.agents import create_agent
from data_retrieval import fetch_odds
from dotenv import load_dotenv

load_dotenv()

agent = create_agent(
    model="claude-sonnet-5",
    tools=[fetch_odds],
    system_prompt="You are a sports betting analyst",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What are the odds on the current summer league NBA games?"}]}
)

agent_message = next(message for message in result["messages"][-1].content_blocks if message["type"] == "text")

print(agent_message["text"])