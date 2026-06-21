from tools import FineCalculatorTool

tool = FineCalculatorTool()

result = tool.invoke(
    {
        "days_overdue": 10,
        "book_type": "regular",
        "membership_tier": "premium"
    }
)

print(result)