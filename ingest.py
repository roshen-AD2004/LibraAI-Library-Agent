import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError(
        "HF_TOKEN not found. Please add it to your .env file."
    )

CATALOG_FILE = "knowledge_base/aether_catalog.txt"
DB_DIRECTORY = "chroma_db"


def main():
    print("Loading catalog...")

    loader = TextLoader(
        CATALOG_FILE,
        encoding="utf-8"
    )

    documents = loader.load()

    print(f"Loaded {len(documents)} document(s)")

    print("Splitting documents...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    print("Loading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={
            "token": HF_TOKEN
        }
    )

    print("Creating Chroma vector store...")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIRECTORY
    )

    print("\nVector store created successfully.")
    print(f"Database saved to: {DB_DIRECTORY}")
    print(f"Total chunks indexed: {len(chunks)}")


if __name__ == "__main__":
    main()