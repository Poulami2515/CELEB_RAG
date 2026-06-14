from src.search.duckduckgo import search_duckduckgo
from src.search.searxng import search_searxng
from src.search.utils import deduplicate_results
from src.models.search_result import SearchResult

def aggregate_search_results(
    query : str,
    max_results : int = 20
) -> list[SearchResult]:
    results = []

    results.extend(search_duckduckgo(query, max_results))
    results.extend(search_searxng(query, max_results))
    return deduplicate_results(results)

def search_all(
    query: str,
    max_results: int = 20
):

    all_results = []

    stats = {}

    try:

        ddg_results = search_duckduckgo(
            query,
            max_results
        )

        stats["duckduckgo"] = len(
            ddg_results
        )

        all_results.extend(
            ddg_results
        )

    except Exception as e:

        print(
            f"DuckDuckGo failed: {e}"
        )

        stats["duckduckgo"] = 0

    try:

        searx_results = search_searxng(
            query,
            max_results
        )

        stats["searxng"] = len(
            searx_results
        )

        all_results.extend(
            searx_results
        )

    except Exception as e:

        print(
            f"SearXNG failed: {e}"
        )

        stats["searxng"] = 0

    before = len(all_results)

    all_results = deduplicate_results(
        all_results
    )

    after = len(all_results)

    stats["merged"] = before

    stats["unique"] = after

    return all_results, stats