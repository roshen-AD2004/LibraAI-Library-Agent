def detect_sentiment(text: str):

    text = text.lower()

    angry_words = [
        "angry",
        "ridiculous",
        "terrible",
        "hate",
        "worst",
        "frustrated"
    ]

    happy_words = [
        "awesome",
        "great",
        "excellent",
        "wonderful",
        "amazing"
    ]

    confused_words = [
        "confused",
        "don't understand",
        "not clear",
        "unclear"
    ]

    for word in angry_words:

        if word in text:
            return "angry"

    for word in happy_words:

        if word in text:
            return "happy"

    for word in confused_words:

        if word in text:
            return "confused"

    return "neutral"