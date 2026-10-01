from agents import agent
from database import create_table

session = True

def main_workflow():
    user_input = input("What is your sports betting question? If you don't have any type 'quit' to exit the program. ")
    if user_input == "quit":
        global session
        session = False
    else:

        result = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]}
                    )
        agent_message = next((message for message in result["messages"][-1].content_blocks if message["type"] == "text"), None)
        response = agent_message["text"] if agent_message else "(The agent didn't return a text response for this turn.)"
        print(response)

if __name__ == "__main__":
    create_table()
    while session is True:
        main_workflow()