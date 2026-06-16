
# src/media/podcast_search.py

from urllib.parse import urlparse

from src.search.aggregator import (
    search_all
)


PODCAST_DOMAINS = {

    "spotify.com",

    "open.spotify.com",

    "podcasts.apple.com",

    "podbean.com",

    "buzzsprout.com",

    "castbox.fm",

    "player.fm",

    "iheart.com",

    "rss.com",

    "simplecast.com",

    "transistor.fm",

    "captivate.fm",

    "jiosaavn.com",

    "gaana.com",

    "wynk.in"
}


def podcast_queries(
    celebrity_name: str
) -> list[str]:
    """
    Generate podcast-focused queries.
    """

    return [

        f"{celebrity_name} podcast",

        f"{celebrity_name} interview podcast",

        f"{celebrity_name} spotify podcast",

        f"{celebrity_name} apple podcast",

        f"{celebrity_name} podcast episode",

        f"{celebrity_name} long interview",

        f"{celebrity_name} audio interview",

        f"{celebrity_name} conversation podcast",

        f"{celebrity_name} podcast appearance",

        f"{celebrity_name} talk show podcast",

        f"{celebrity_name} guest podcast"
    ]


def is_podcast_url(
    url: str
) -> bool:
    """
    Determine whether a URL belongs
    to a podcast platform.
    """

    try:

        domain = (
            urlparse(url)
            .netloc
            .lower()
        )

        return any(

            podcast_domain in domain

            for podcast_domain
            in PODCAST_DOMAINS
        )

    except Exception:

        return False


def deduplicate_podcast_results(
    results: list
) -> list:
    """
    Remove duplicate URLs.
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


def search_podcast_urls(
    celebrity_name: str,
    max_results: int = 20
) -> list:
    """
    Search podcast URLs for a celebrity.
    """

    queries = podcast_queries(
        celebrity_name
    )

    all_results = []

    for query in queries:

        print(
            f"Searching podcast query: "
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

    podcast_results = [

    result

    for result in all_results

    if is_podcast_url(result.url)

    and

    is_podcast_episode(result.url)
]

    podcast_results = (
        deduplicate_podcast_results(
            podcast_results
        )
    )

    print(
        f"Found "
        f"{len(podcast_results)} "
        f"unique podcast URLs"
    )

    return podcast_results[
        :max_results
    ]

def is_podcast_episode(
    url: str
) -> bool:

    url = url.lower()

    return (

        "/episode/" in url

        or

        "podcasts.apple.com" in url
        and "?i=" in url
    )

def print_podcast_results(
    podcast_results: list
):
    """
    Pretty-print podcast results.
    """

    print()

    for index, result in enumerate(

        podcast_results,

        start=1
    ):

        print(
            f"{index}. "
            f"{result.title}"
        )

        print(
            result.url
        )

        print()