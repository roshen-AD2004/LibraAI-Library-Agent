from tools import borrow_action

print(
    borrow_action.invoke(
        {
            "user_id": "U1001",
            "book_title_or_isbn": "Atomic Habits",
            "action_type": "borrow"
        }
    )
)