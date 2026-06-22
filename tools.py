from urllib import response
from datetime import datetime, timedelta

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
def catalog_search(query: str) -> str:
    """
    Search the Aether Library catalog and policy database.

    Use this tool whenever a user asks about:
    - Books
    - Authors
    - Genres
    - ISBNs
    - Membership rules
    - Renewals
    - Reservations
    - Library policies

    Do not use this tool for current availability, borrower status, or copy counts.
    Use book_status for all availability and inventory queries.
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
        response.append("\nSource: aether_catalog.txt")
        response.append("\nSection: BOOK_ENTRY")
        response.append("")

    return "\n".join(response)

@tool
def borrow_action(
    user_id: str,
    book_title_or_isbn: str,
    action_type: str
) -> str:
    """
    Process borrow or reserve actions.

    Inputs:
    - user_id
    - book_title_or_isbn
    - action_type (borrow, reserve)

    Updates:
    - books.json
    - members.json
    - transactions.log
    """

    action_type = action_type.lower()

    if action_type not in ["borrow", "reserve"]:
        return (
            "Invalid action type. "
            "Supported actions: borrow, reserve"
        )

    try:

        with open(
            "data/books.json",
            "r",
            encoding="utf-8"
        ) as f:

            books = json.load(f)

        with open(
            "data/members.json",
            "r",
            encoding="utf-8"
        ) as f:

            members = json.load(f)

        target_book = None

        for book in books:

            if (
                book["title"].lower()
                == book_title_or_isbn.lower()
                or
                book["isbn"]
                == book_title_or_isbn
            ):

                target_book = book
                break

        if target_book is None:
            return "Book not found."

        target_member = None

        for member in members:

            if member["user_id"].lower() == user_id.lower():

                target_member = member
                break

        if target_member is None:
            return "Member not found."

        # --------------------
        # BORROW
        # --------------------

        if action_type == "borrow":

            if target_book["available_copies"] <= 0:

                return (
                    f"No copies of "
                    f"'{target_book['title']}' "
                    f"are currently available. "
                    f"Please reserve the book."
                )

            due_date = (
                datetime.utcnow()
                +
                timedelta(
                    days=target_book[
                        "borrow_period_days"
                    ]
                )
            ).strftime("%Y-%m-%d")

            target_book[
                "available_copies"
            ] -= 1

            target_book[
                "borrowers"
            ].append(
                {
                    "user_id": user_id,
                    "due_date": due_date
                }
            )

            target_member[
                "borrowed_books"
            ].append(
                {
                    "title": target_book["title"],
                    "due_date": due_date
                }
            )

            transaction = {
                "timestamp":
                datetime.utcnow().isoformat(),

                "action": "borrow",

                "user_id": user_id,

                "book":
                target_book["title"],

                "due_date":
                due_date
            }

            with open(
                "data/books.json",
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    books,
                    f,
                    indent=4
                )

            with open(
                "data/members.json",
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    members,
                    f,
                    indent=4
                )

            with open(
                "data/transactions.log",
                "a",
                encoding="utf-8"
            ) as f:

                f.write(
                    json.dumps(
                        transaction
                    )
                    + "\n"
                )

            return (
                f"SUCCESS: Borrow completed.\n\n"
                f"User ID: {user_id}\n"
                f"Book: {target_book['title']}\n"
                f"Due Date: {due_date}\n"
                f"Remaining Copies: "
                f"{target_book['available_copies']}"
            )

        # --------------------
        # RESERVE
        # --------------------

        if action_type == "reserve":

            if (
                user_id
                in target_book[
                    "reservation_queue"
                ]
            ):

                return (
                    "User already exists "
                    "in reservation queue."
                )

            target_book[
                "reservation_queue"
            ].append(
                user_id
            )

            target_member[
                "reservations"
            ].append(
                target_book["title"]
            )

            transaction = {
                "timestamp":
                datetime.utcnow().isoformat(),

                "action":
                "reserve",

                "user_id":
                user_id,

                "book":
                target_book["title"]
            }

            with open(
                "data/books.json",
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    books,
                    f,
                    indent=4
                )

            with open(
                "data/members.json",
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    members,
                    f,
                    indent=4
                )

            with open(
                "data/transactions.log",
                "a",
                encoding="utf-8"
            ) as f:

                f.write(
                    json.dumps(
                        transaction
                    )
                    + "\n"
                )

            position = len(
                target_book[
                    "reservation_queue"
                ]
            )

            return (
                f"Reservation successful.\n\n"
                f"Book: {target_book['title']}\n"
                f"User ID: {user_id}\n"
                f"Queue Position: {position}"
            )

    except Exception as e:

        return (
            f"Transaction failed: "
            f"{str(e)}"
        )


@tool
def fine_calculator(
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
def borrow_action(
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

@tool
def membership_status(user_id: str) -> str:
    """
    Check complete membership information.

    Use when user asks:
    - membership status
    - membership details
    - membership tier
    - active membership
    - borrowed books
    - reservations
    - fines
    """

    try:

        with open(
            "data/members.json",
            "r",
            encoding="utf-8"
        ) as f:

            members = json.load(f)

        for member in members:

            if member["user_id"].lower() == user_id.lower():

                borrowed_books = member.get(
                    "borrowed_books",
                    []
                )

                reservations = member.get(
                    "reservations",
                    []
                )

                borrowed_text = []

                for book in borrowed_books:

                    borrowed_text.append(
                        f"- {book['title']} "
                        f"(Due: {book['due_date']})"
                    )

                reservation_text = []

                for reservation in reservations:

                    reservation_text.append(
                        f"- {reservation}"
                    )

                return (
                    f"Membership Information\n\n"
                    f"User ID: {member['user_id']}\n"
                    f"Name: {member['name']}\n"
                    f"Tier: {member['tier']}\n"
                    f"Active: {member['active']}\n\n"
                    f"Borrowed Books:\n"
                    f"{chr(10).join(borrowed_text) if borrowed_text else 'None'}\n\n"
                    f"Reservations:\n"
                    f"{chr(10).join(reservation_text) if reservation_text else 'None'}\n\n"
                    f"Current Fine: ${member.get('current_fines', 0)}"
                )

        return f"No member found with User ID '{user_id}'."

    except FileNotFoundError:
        return "members.json file not found."

    except Exception as e:
        return f"Error reading membership information: {str(e)}"
    
@tool
def return_book(
    user_id: str,
    book_title: str
) -> str:
    """
    Return a borrowed book.

    Updates:
    - books.json
    - members.json
    - transactions.log
    """

    import json
    from datetime import datetime

    with open(
        "data/books.json",
        "r",
        encoding="utf-8"
    ) as f:
        books = json.load(f)

    with open(
        "data/members.json",
        "r",
        encoding="utf-8"
    ) as f:
        members = json.load(f)

    target_book = None

    for book in books:

        if book["title"].lower() == book_title.lower():
            target_book = book
            break

    if not target_book:
        return "Book not found."

    borrower_found = False

    updated_borrowers = []

    for borrower in target_book["borrowers"]:

        if borrower["user_id"] == user_id:
            borrower_found = True
        else:
            updated_borrowers.append(
                borrower
            )

    if not borrower_found:
        return (
            "This user has not borrowed "
            "the specified book."
        )

    target_book["borrowers"] = (
        updated_borrowers
    )

    target_book["available_copies"] += 1

    for member in members:

        if member["user_id"] == user_id:

            member["borrowed_books"] = [

                b for b in
                member["borrowed_books"]

                if b["title"].lower()
                != book_title.lower()

            ]

            break

    with open(
        "data/books.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            books,
            f,
            indent=4
        )

    with open(
        "data/members.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            members,
            f,
            indent=4
        )

    transaction = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "book": book_title,
        "action": "return"
    }

    with open(
        "data/transactions.log",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(transaction)
            + "\n"
        )

    return (
        f"SUCCESS: Return completed.\n"
        f"Book: {book_title}\n"
        f"Available Copies: "
        f"{target_book['available_copies']}"
    )


def _who_has_book(book_title_or_isbn: str) -> str:
    """
    Raw implementation for book borrower and availability lookup.
    """
    try:
        with open("data/books.json", "r", encoding="utf-8") as f:
            books = json.load(f)

        with open("data/members.json", "r", encoding="utf-8") as f:
            members = json.load(f)

        target = None
        for b in books:
            if b.get("title", "").lower() == book_title_or_isbn.lower() or b.get("isbn") == book_title_or_isbn:
                target = b
                break

        if not target:
            return "Book not found."

        borrowers = target.get("borrowers", [])
        reservation_queue = target.get("reservation_queue", [])

        lines = [
            f"Book: {target.get('title')} ({target.get('available_copies')}/{target.get('total_copies')} available)"
        ]

        if borrowers:
            lines.append("Current borrowers:")
            for br in borrowers:
                uid = br.get("user_id")
                due = br.get("due_date", "unknown")
                name = None
                for m in members:
                    if m.get("user_id") == uid:
                        name = m.get("name")
                        break
                lines.append(f"- {uid}{f' ({name})' if name else ''} — Due: {due}")
        else:
            lines.append("No current borrowers.")

        if reservation_queue:
            lines.append(f"Reservation queue ({len(reservation_queue)}): {', '.join(reservation_queue)}")
        else:
            lines.append("No reservations.")

        return "\n".join(lines)

    except FileNotFoundError:
        return "Required data files not found."

    except Exception as e:
        return f"Error checking borrowers: {str(e)}"


@tool
def who_has_book(book_title_or_isbn: str) -> str:
    """
    Return current borrowers, due dates, availability and reservation queue for a book.
    """
    return _who_has_book(book_title_or_isbn)


@tool
def book_status(book_title_or_isbn: str) -> str:
    """
    Return current availability, borrowers, due dates, and reservation queue for a book.
    """
    return _who_has_book(book_title_or_isbn)


def _who_borrowed_by_user(user_id: str) -> str:
    """
    Raw implementation for member loan lookup.
    """
    try:
        with open("data/members.json", "r", encoding="utf-8") as f:
            members = json.load(f)

        for member in members:
            if member.get("user_id", "").lower() == user_id.lower():
                borrowed = member.get("borrowed_books", [])
                if not borrowed:
                    return f"User {user_id} has no active borrowed books."

                lines = [f"User: {member.get('user_id')} ({member.get('name')})"]
                lines.append("Borrowed books:")
                for b in borrowed:
                    title = b.get("title")
                    due = b.get("due_date", "unknown")
                    lines.append(f"- {title} — Due: {due}")

                return "\n".join(lines)

        return f"No member found with User ID '{user_id}'."

    except FileNotFoundError:
        return "members.json file not found."

    except Exception as e:
        return f"Error reading member loans: {str(e)}"


@tool
def who_borrowed_by_user(user_id: str) -> str:
    """
    Return what a given user currently has borrowed.

    Use when user asks:
    - what do I have checked out
    - what has USER_ID borrowed
    """
    return _who_borrowed_by_user(user_id)


@tool
def member_lookup(user_id: str) -> str:
    """
    Return member loan and reservation details by user ID.
    """
    return _who_borrowed_by_user(user_id)


@tool
def handle_dispute(user_id: str, issue: str) -> str:
    """
    Log a dispute and redirect the user to human library staff.

    Use when user files a dispute, reports damage, or requests human escalation.
    """

    try:
        transaction = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "action": "dispute",
            "issue": issue
        }

        with open("data/transactions.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(transaction) + "\n")

        # Redirect to human staff
        return (
            "Your dispute has been recorded and escalated to library staff. "
            "Please contact the library front desk or email the support team for further assistance. "
            "A staff member will review your case shortly."
        )

    except Exception as e:
        return f"Failed to record dispute: {str(e)}"