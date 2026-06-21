from langchain_core.tools import BaseTool
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from pydantic import Field

class CatalogSearchTool(BaseTool):
    name: str = "catalog_search"
    description: str = (
        "Searches the Aether Library catalog and policy database. "
        "Use this tool whenever a user asks about books, availability, authors, genres, "
        "library policies, membership rules, renewals, reservations, or ISBN information."
    )

    db_path: str = Field(default="chroma_db")

    def _run(self, query: str) -> str:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vectorstore = Chroma(
            persist_directory=self.db_path,
            embedding_function=embeddings
        )

        results = vectorstore.similarity_search(query, k=3)

        if not results:
            return "No matching catalog entries found."

        response = []

        for idx, doc in enumerate(results, start=1):
            response.append(f"Result {idx}")
            response.append(doc.page_content)
            response.append("\n")

        return "\n".join(response)