from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import json
from datetime import datetime


# Load embedding model ONCE
EMBEDDINGS = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


@tool
def CatalogSearchTool(query: str) -> str:
    """
    Search the Aether Library catalog and policy database.

    Use this tool whenever a user asks about:
    - Books
    - Authors
    - Genres
    - Availability
    - ISBNs
    - Membership rules
    - Renewals
    - Reservations
    - Library policies
    """

    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=EMBEDDINGS
    )

    results = vectorstore.similarity_search(query, k=3)

    if not results:
        return "No matching catalog entries found."

    response = []

    for idx, doc in enumerate(results, start=1):
        response.append(f"Result {idx}")
        response.append("-" * 50)
        response.append(doc.page_content)
        response.append("")

    return "\n".join(response)


@tool
def FineCalculatorTool(
    days_overdue: int,
    book_type: str,
    membership_tier: str = "standard"
) -> str:
    """
    Calculate overdue fines.

    Parameters:
    - days_overdue: number of overdue days
    - book_type: regular or new_release
    - membership_tier: standard or premium
    """

    rates = {
        "regular": 0.50,
        "new_release": 2.00
    }

    rate = rates.get(book_type.lower())

    if rate is None:
        return (
            "Unknown book type. "
            "Supported types: regular, new_release"
        )

    fine = days_overdue * rate

    if membership_tier.lower() == "premium":
        fine *= 0.5

    return (
        f"Fine Calculation\n"
        f"Days Overdue: {days_overdue}\n"
        f"Book Type: {book_type}\n"
        f"Membership Tier: {membership_tier}\n"
        f"Total Fine: ${fine:.2f}"
    )

@tool
def BorrowActionTool(
    user_id: str,
    book_title_or_isbn: str,
    action_type: str,
    days: int = 0
) -> str:
    """
    Process borrow, renew, or reserve actions.

    action_type must be:
    - borrow
    - renew
    - reserve
    """

    valid_actions = [
        "borrow",
        "renew",
        "reserve"
    ]

    if action_type.lower() not in valid_actions:
        return (
            "Invalid action type. "
            "Allowed values: borrow, renew, reserve."
        )

    # Prevent duplicate transactions
    if os.path.exists("transactions.log"):

        with open(
            "transactions.log",
            "r",
            encoding="utf-8"
        ) as f:

            lines = f.readlines()

        if lines:

            last_transaction = json.loads(
                lines[-1]
            )

            if (
                last_transaction["user_id"] == user_id
                and last_transaction["book"] == book_title_or_isbn
                and last_transaction["action"] == action_type.lower()
            ):

                return (
                    "Duplicate transaction detected. "
                    "Transaction already processed."
                )

    transaction = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "book": book_title_or_isbn,
        "action": action_type.lower(),
        "days": days
    }

    with open(
        "transactions.log",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(transaction) + "\n"
        )

    return (
        f"SUCCESS: {action_type.capitalize()} completed.\n"
        f"User ID: {user_id}\n"
        f"Book: {book_title_or_isbn}\n"
        f"Days: {days}\n"
        f"No further action required."
    )