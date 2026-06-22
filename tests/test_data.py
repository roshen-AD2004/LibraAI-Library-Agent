import json

with open(
    "data/books.json",
    "r",
    encoding="utf-8"
) as f:

    books = json.load(f)

print("Books Loaded:", len(books))

for book in books:

    print(
        book["title"],
        "| Available:",
        book["available_copies"]
    )