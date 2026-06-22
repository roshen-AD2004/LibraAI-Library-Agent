from tools import return_book

result = return_book.invoke(
    {
        "user_id": "U1001",
        "book_title": "Dune"
    }
)

print(result)