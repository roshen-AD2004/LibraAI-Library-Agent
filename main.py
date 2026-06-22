import os

from dotenv import load_dotenv

from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from sentiment import detect_sentiment
from escalation import requires_escalation

from prompts import SYSTEM_PROMPT

from tools import (
    catalog_search,
    fine_calculator,
    borrow_action,
    membership_status
)


load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

tools = [
    catalog_search,
    fine_calculator,
    borrow_action,
    membership_status
]

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT
)

print(type(agent))

print("LibraAI Started")
print("Type 'exit' to quit.\n")

while True:

    user_input = input("You: ")

    sentiment = detect_sentiment(
        user_input
    )

    if sentiment == "angry":

        print(
            "\nLibraAI:"
        )

        print(
            "I'm sorry you're frustrated."
        )

    elif sentiment == "happy":

        print(
            "\nLibraAI:"
        )

        print(
            "That's wonderful!"
        )

    elif sentiment == "confused":

        print(
            "\nLibraAI:"
        )

        print(
            "Let me explain clearly."
        )

    if user_input.lower() == "exit":
        break

    if requires_escalation(user_input):

        print(
            "\nLibraAI:"
        )

        print(
            "This request requires assistance "
            "from a human librarian."
        )

        continue

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        }
    )

    print("\nLibraAI:")

    print(result["messages"][-1].content)

    print()