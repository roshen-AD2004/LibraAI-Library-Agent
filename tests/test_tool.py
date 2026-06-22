from tools import catalog_search

print(catalog_search.args)

result = catalog_search.invoke(
    {"query": "George Orwell"}
)

print(result)