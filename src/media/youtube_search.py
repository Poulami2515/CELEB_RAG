# src/media/youtube_search.py

from src.search.aggregator import (
    search_all
)


def youtube_queries(
    celebrity_name: str
) -> list[str]:
    """
    Generate YouTube-focused search queries.
    """

    return [

        f"{celebrity_name} interview youtube",

        f"{celebrity_name} podcast youtube",

        f"{celebrity_name} speech youtube",

        f"{celebrity_name} conversation youtube",

        f"{celebrity_name} talk youtube",

        f"{celebrity_name} latest interview youtube",

        f"{celebrity_name} career interview youtube",

        f"{celebrity_name} motivational speech youtube",

        f"{celebrity_name} film companion youtube",

        f"{celebrity_name} ted talk youtube"
    ]


def is_youtube_url(
    url: str
) -> bool:
    """
    Check whether a URL belongs to YouTube.
    """

    url = url.lower()

    return (

        "youtube.com/watch" in url

        or

        "youtu.be/" in url
    )


def deduplicate_youtube_results(
    results: list
) -> list:
    """
    Remove duplicate YouTube URLs.
    """

    seen_urls = set()

    unique_results = []

    for result in results:

        if result.url in seen_urls:

            continue

        seen_urls.add(
            result.url
        )

        unique_results.append(
            result
        )

    return unique_results


def search_youtube_urls(
    celebrity_name: str,
    max_results: int = 20
) -> list:
    """
    Search YouTube URLs for a celebrity.
    """

    queries = youtube_queries(
        celebrity_name
    )

    all_results = []

    for query in queries:

        print(
            f"Searching YouTube query: "
            f"{query}"
        )

        try:

            results, stats = (
                search_all(query)
            )

            all_results.extend(
                results
            )

        except Exception as e:

            print(
                f"Search failed: {e}"
            )

    youtube_results = [

        result

        for result in all_results

        if is_youtube_url(
            result.url
        )
    ]

    youtube_results = (
        deduplicate_youtube_results(
            youtube_results
        )
    )

    print(
        f"Found "
        f"{len(youtube_results)} "
        f"unique YouTube URLs"
    )

    return youtube_results[
        :max_results
    ]


def print_youtube_results(
    youtube_results: list
):
    """
    Pretty-print results.
    """

    print()

    for i, result in enumerate(
        youtube_results,
        start=1
    ):

        print(
            f"{i}. {result.title}"
        )

        print(
            result.url
        )

        print()