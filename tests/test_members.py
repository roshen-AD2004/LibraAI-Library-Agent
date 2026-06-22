import json

with open(
    "data/members.json",
    "r",
    encoding="utf-8"
) as f:

    members = json.load(f)

for member in members:

    print(
        member["user_id"],
        member["name"]
    )