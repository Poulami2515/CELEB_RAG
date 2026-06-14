import json
from pathlib import Path

from src.models.search_result import SearchResult

def save_results(
    celebrity_name : str,
    results : list[SearchResult]
):
    folder = Path("data") / celebrity_name.lower().replace(" ", "_")
    folder.mkdir(
        parents = True,
        exist_ok = True
    )

    file_path = folder/"search_results.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            [r.model_dump() for r in results],
            f,
            indent = 4,
            ensure_ascii = False
        )