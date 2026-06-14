from urllib.parse import urlparse
from src.models.search_result import SearchResult

def normalize_url(url : str):
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return f"{netloc}{parsed.path}"

def deduplicate_results(
    results: list[SearchResult],
) :
    seen = set()
    unique = []

    for result in results:
        normalized = normalize_url(result.url)
        if normalized not in seen:
            seen.add(normalized)
            unique.append(result)

    return unique
