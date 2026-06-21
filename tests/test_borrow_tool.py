from tools import BorrowActionTool

tool = BorrowActionTool()

result = tool.invoke(
    {
        "user_id": "1001",
        "book_title_or_isbn": "Dune",
        "action_type": "borrow"
    }
)

print(result)