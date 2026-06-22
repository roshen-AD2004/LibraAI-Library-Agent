from tools import catalog_search

queries = [
    "science fiction",
    "finance",
    "romance"
]

for query in queries:

    print("=" * 50)

    print(
        f"QUERY: {query}"
    )

    result = catalog_search.invoke(
        {
            "query": query
        }
    )

    print(result)