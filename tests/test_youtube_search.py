from src.media.youtube_search import (
    search_youtube_urls,
    print_youtube_results
)


results = search_youtube_urls(
    "Shah Rukh Khan"
)

print_youtube_results(
    results
)