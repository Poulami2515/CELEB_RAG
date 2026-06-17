# src/media/instagram_search.py

from urllib.parse import (
    urlparse,
    urlunparse
)

from src.search.aggregator import (
    search_all
)


def instagram_queries(
    celebrity_name: str
) -> list[str]:
    """
    Generate Instagram-focused queries.
    """

    return [

        f"site:instagram.com {celebrity_name}",

        f"site:instagram.com {celebrity_name} instagram",

        f"site:instagram.com {celebrity_name} reel",

        f"site:instagram.com {celebrity_name} post",

        f"site:instagram.com {celebrity_name} official",

        f"site:instagram.com {celebrity_name} photos",

        f"site:instagram.com {celebrity_name} videos",

        f"{celebrity_name} instagram"
    ]


def is_instagram_url(
    url: str
) -> bool:
    """
    Check whether URL belongs
    to Instagram.
    """

    return (
        "instagram.com"
        in url.lower()
    )


def normalize_instagram_url(
    url: str
) -> str:
    """
    Remove query parameters
    and trailing slashes.
    """

    parsed = urlparse(url)

    return urlunparse(

        (
            parsed.scheme,

            parsed.netloc.lower(),

            parsed.path.rstrip("/"),

            "",

            "",

            ""
        )
    )

import re


def extract_follower_count(
    snippet: str
) -> int:
    """
    Extract follower count from search snippet.

    Examples:
    49M Followers
    367K Followers
    152 Followers
    """

    if not snippet:
        return 0

    snippet = snippet.lower()

    match = re.search(
        r'([\d\.]+)\s*([mk]?)\s*followers',
        snippet
    )

    if not match:
        return 0

    number = float(
        match.group(1)
    )

    suffix = (
        match.group(2)
    )

    if suffix == "m":
        number *= 1_000_000

    elif suffix == "k":
        number *= 1_000

    return int(number)


def deduplicate_instagram_results(
    results: list
) -> list:
    """
    Remove duplicate Instagram URLs.
    """

    seen_urls = set()

    unique_results = []

    for result in results:

        normalized_url = (
            normalize_instagram_url(
                result.url
            )
        )

        if normalized_url in seen_urls:

            continue

        seen_urls.add(
            normalized_url
        )

        unique_results.append(
            result
        )

    return unique_results


def search_instagram_urls(
    celebrity_name: str,
    max_results: int = 20
) -> list:
    """
    Search Instagram URLs
    related to a celebrity.
    """

    queries = (
        instagram_queries(
            celebrity_name
        )
    )

    all_results = []

    for query in queries:

        print(
            f"Searching Instagram: "
            f"{query}"
        )

        try:

            results, stats = (
                search_all(
                    query
                )
            )

            all_results.extend(
                results
            )

        except Exception as e:

            print(
                f"Instagram search failed: "
                f"{e}"
            )

    instagram_results = [

        result

        for result

        in all_results

        if is_instagram_url(
            result.url
        )
    ]

    instagram_results = (
        deduplicate_instagram_results(
            instagram_results
        )
    )

    instagram_results = (
    keep_official_content(
        instagram_results
        )
    )

    instagram_results.sort(

        key=lambda result:

        (
            "/reel/" in result.url.lower()

            or

            "/p/" in result.url.lower()
        )
    )

    print(

        f"Found "

        f"{len(instagram_results)} "

        f"unique Instagram URLs"
    )

    return instagram_results[
        :max_results
    ]


def print_instagram_results(
    instagram_results: list
):
    """
    Pretty-print Instagram results.
    """

    print()

    for index, result in enumerate(

        instagram_results,

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


def extract_username(
    url: str
) -> str:

    try:

        path = (
            urlparse(url)
            .path
            .strip("/")
        )

        if not path:
            return ""

        username = path.split("/")[0]

        if username in {

            "p",

            "reel",

            "explore",

            "stories"

        }:

            return ""

        return username.lower()

    except Exception:

        return ""


def find_official_profile(
    instagram_results: list
):
    """
    Choose the profile with
    the highest follower count.
    """

    best_profile = None

    best_followers = -1

    for result in instagram_results:

        url = result.url.lower()

        if (

            "/p/" in url

            or

            "/reel/" in url

        ):

            continue

        followers = extract_follower_count(
            result.snippet
        )

        if followers > best_followers:

            best_followers = followers

            best_profile = result

    return best_profile


def keep_official_content(
    instagram_results: list
):
    """
    Keep

    - Official profile

    - Posts

    - Reels

    from that profile only.
    """

    official = find_official_profile(
        instagram_results
    )

    if official is None:

        return []

    username = extract_username(
        official.url
    )

    filtered = [

        official
    ]

    for result in instagram_results:

        url = result.url.lower()

        if (

            f"instagram.com/{username}/"

            not in url

        ):

            continue

        if (

            "/p/" in url

            or

            "/reel/" in url

        ):

            filtered.append(
                result
            )

    return filtered