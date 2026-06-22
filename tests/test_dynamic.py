import json
import os

with open(
    "data/books.json",
    "r",
    encoding="utf-8"
) as f:

    books = json.load(f)

print("Books:", len(books))

with open(
    "data/members.json",
    "r",
    encoding="utf-8"
) as f:

    members = json.load(f)

print("Members:", len(members))

print(
    "Transaction File Exists:",
    os.path.exists(
        "data/transactions.log"
    )
)