from tools import membership_status

result = membership_status.invoke(
    {
        "user_id": "U1001"
    }
)

print(result)