from ddgs import DDGS

from src.models.search_result import SearchResult


def search_duckduckgo(
    query: str,
    max_results: int = 30,
) -> list[SearchResult]:
    results: list[SearchResult] = []

    with DDGS() as ddgs:
        for item in ddgs.text(query, max_results=max_results):
            title = item.get("title")
            url = item.get("href")
            snippet = item.get("body", "")

            if title and url:
                results.append(
                    SearchResult(
                        title=title,
                        url=url,
                        snippet=snippet,
                        source="duckduckgo",
                    )
                )

    return results
