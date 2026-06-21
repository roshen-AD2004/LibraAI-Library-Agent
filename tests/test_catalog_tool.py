import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tools import CatalogSearchTool

tool = CatalogSearchTool

result = tool.invoke(
    {
        "query": "renewal policy for overdue books"
    }
)

print(result)