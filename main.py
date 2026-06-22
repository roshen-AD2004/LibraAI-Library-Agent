import os

from dotenv import load_dotenv

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from sentiment import detect_sentiment
from escalation import requires_escalation

from prompts import SYSTEM_PROMPT

from tools import (
    catalog_search,
    fine_calculator,
    borrow_action,
    membership_status,
    return_book
)

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-oss-120b:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)

tools = [
    catalog_search,
    fine_calculator,
    borrow_action,
    membership_status,
    return_book
]

memory = MemorySaver()

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT,
    checkpointer=memory
)

print(type(agent))

print("LibraAI Started")
print("Type 'exit' to quit.\n")

config = {
    "configurable": {
        "thread_id": "library_user"
    }
}

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
        },
        config=config
    )

    print("\nLibraAI:")

    print(result["messages"][-1].content)

    print()