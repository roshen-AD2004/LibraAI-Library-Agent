# LibraAI – Policy-Driven Library Management Agent

LibraAI is an AI-powered librarian assistant for the fictional **Aether Library**. It uses Retrieval-Augmented Generation (RAG), vector search, tool-calling, memory, and policy-driven reasoning to help users search books, manage memberships, calculate fines, borrow books, reserve books, and access library information.

## Features

* Book Search using ChromaDB Vector Database
* Library Policy Search
* Membership Status Lookup
* Fine Calculation
* Borrow / Renew / Reserve Books
* Transaction Logging
* Source-Cited Responses
* Sentiment-Aware Conversations
* Conversation Memory
* OpenRouter LLM Integration
* Gradio Web Interface
* Docker Support

---

## Tech Stack

* Python 3.10.11
* LangChain
* LangGraph
* ChromaDB
* HuggingFace Embeddings
* OpenRouter
* GPT-OSS-120B
* Gradio
* Docker

---

## Project Structure

```text
LibraAI/
│
├── main.py
├── app.py
├── tools.py
├── prompts.py
├── ingest.py
├── sentiment.py
├── escalation.py
│
├── knowledge_base/
│   └── aether_catalog.txt
│
├── data/
│   ├── books.json
│   ├── members.json
│   └── transactions.log
│
├── chroma_db/
│
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd LibraAI
```

### Create Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / Mac:

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```env
OPENROUTER_API_KEY=your_api_key_here
```

---

## Build Vector Database

Run the ingestion script:

```bash
python ingest.py
```

Expected Output:

```text
Documents loaded successfully.
Chunks created successfully.
Embeddings generated successfully.
Chroma database persisted successfully.
```

---

## Run LibraAI (Terminal Version)

```bash
python main.py
```

Expected Output:

```text
LibraAI Started
Type 'exit' to quit.
```

Example:

```text
You: Find Dune

LibraAI:
Dune by Frank Herbert is available.

Source: aether_catalog.txt
Section: BOOK_ENTRY
```

---

## Run Gradio Interface

```bash
python app.py
```

Expected Output:

```text
Running on local URL:
http://127.0.0.1:7860
```

Open the URL in your browser.

---

## Docker

### Build Docker Image

```bash
docker build -t libraai .
```

### Run Container

```bash
docker run -p 7860:7860 libraai
```

---

## Example Questions

### Book Search

```text
Find science fiction books.
```

```text
Who wrote Dune?
```

```text
Is 1984 available?
```

### Membership

```text
My user ID is U1001.
```

```text
Check my membership status.
```

### Fine Calculation

```text
Calculate fine for 10 overdue days on a regular book.
```

### Borrowing

```text
Borrow Dune.
```

```text
Reserve The Hobbit.
```

```text
Renew Dune.
```

---

## Future Enhancements

* Dynamic Return System
* Automatic Waitlist Processing
* Overdue Book Detection
* Fine Tracking
* Library Analytics Dashboard
* Multi-User Support
* Admin Panel
* Streamlit Frontend
