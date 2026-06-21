import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from tools import (
    CatalogSearchTool,
    FineCalculatorTool,
    BorrowActionTool
)

from prompts import SYSTEM_PROMPT

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

agent = create_react_agent(
    model=llm,
    tools=[
        CatalogSearchTool,
        FineCalculatorTool,
        BorrowActionTool
    ],
    prompt=SYSTEM_PROMPT
)

queries = [
    "Find Dune",
    "Who wrote Dune?",
    "Calculate fine for regular book 5 days overdue"
]

for query in queries:

    print("\n" + "=" * 60)

    print("Query:", query)

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
    )

    print(result["messages"][-1].content)