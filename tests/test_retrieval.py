from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


DB_DIRECTORY = "chroma_db"


def main():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory=DB_DIRECTORY,
        embedding_function=embeddings
    )

    query = "late fees and fines"

    results = vectorstore.similarity_search(
        query=query,
        k=3
    )

    print(f"\nQuery: {query}")
    print("-" * 50)

    for idx, doc in enumerate(results, start=1):
        print(f"\nResult {idx}")
        print(doc.page_content[:400])


if __name__ == "__main__":
    main()