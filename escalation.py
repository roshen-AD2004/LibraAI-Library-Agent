def requires_escalation(text: str):

    text = text.lower()

    keywords = [
        "membership dispute",
        "payment dispute",
        "appeal",
        "account complaint",
        "refund"
    ]

    for keyword in keywords:

        if keyword in text:
            return True

    return False