# tests/test_instagram_search.py

from src.search.aggregator import (
    search_all
)

results, stats = search_all(
    "site:instagram.com Shah Rukh Khan"
)

for result in results[:20]:

    print(result.title)
    print(result.url)
    print()