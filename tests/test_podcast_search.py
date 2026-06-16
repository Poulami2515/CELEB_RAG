# tests/test_podcast_search.py

from src.media.podcast_search import (
    search_podcast_urls,
    print_podcast_results
)

results = search_podcast_urls(
    "Shah Rukh Khan"
)

print_podcast_results(
    results
)