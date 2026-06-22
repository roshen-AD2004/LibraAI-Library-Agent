import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tools import catalog_search

tool = catalog_search

result = tool.invoke(
    {
        "query": "Dune"
    }
)

print(result)