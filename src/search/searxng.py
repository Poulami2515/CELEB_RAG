import os
import requests

from dotenv import load_dotenv

from src.models.search_result import SearchResult

load_dotenv()

SEARXNG_URL = os.getenv(
    "SEARXNG_URL",
    "https://searx.be"
)

#test = http://localhost:8080/search?q=test&format=json

def search_searxng(
    query : str,
    max_results : int = 20
) -> list[SearchResult]:
    url = f"{SEARXNG_URL}/search"

    params = {
        "q" : query,
        "format" : "json"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers={
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ),
            },
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()

    except Exception as e:
        print(f"SearXNG error : {e}")
        return []

    results = []

    for item in data.get("results", []):
        results.append(
            SearchResult(
                title = item.get("title", ""),
                url = item.get("url", ""),
                snippet = item.get("content", ""),
                source = "searxng"
            )
        )

    return results[:max_results]