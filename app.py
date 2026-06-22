import gradio as gr

from agent_builder import get_agent

from sentiment import detect_sentiment
from escalation import requires_escalation

agent = get_agent()

config = {
    "configurable": {
        "thread_id": "gradio_user"
    }
}


def chat(message, history):

    sentiment = detect_sentiment(message)

    sentiment_response = ""

    if sentiment == "angry":
        sentiment_response = (
            "I'm sorry you're frustrated.\n\n"
        )

    elif sentiment == "happy":
        sentiment_response = (
            "That's wonderful!\n\n"
        )

    elif sentiment == "confused":
        sentiment_response = (
            "Let me explain clearly.\n\n"
        )

    if requires_escalation(message):

        return (
            sentiment_response +
            "This request requires assistance from a human librarian."
        )

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        },
        config=config
    )

    answer = result["messages"][-1].content

    return sentiment_response + answer


demo = gr.ChatInterface(
    fn=chat,
    title="📚 LibraAI",
    description=(
        "Policy-Driven Library Management Agent "
        "for Aether Library"
    ),
    chatbot=gr.Chatbot(height=500)
)

demo.launch()