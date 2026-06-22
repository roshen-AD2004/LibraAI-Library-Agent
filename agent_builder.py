import os

from dotenv import load_dotenv

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from langchain_openai import ChatOpenAI

from prompts import SYSTEM_PROMPT

from tools import (
    catalog_search,
    fine_calculator,
    borrow_action,
    membership_status,
    who_has_book,
    who_borrowed_by_user,
    handle_dispute,
    book_status,
    member_lookup
)

load_dotenv()

memory = MemorySaver()

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
    who_has_book,
    who_borrowed_by_user,
    handle_dispute,
    book_status,
    member_lookup
]

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT,
    checkpointer=memory
)


def get_agent():
    return agent