import os

from dotenv import load_dotenv

from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

from tools import (
    CatalogSearchTool,
    FineCalculatorTool,
    BorrowActionTool,
)

from prompts import SYSTEM_PROMPT


load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

tools = [
    CatalogSearchTool,
    FineCalculatorTool,
    BorrowActionTool,
]

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT
)

print("LibraAI Started")
print("Type 'exit' to quit.\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

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