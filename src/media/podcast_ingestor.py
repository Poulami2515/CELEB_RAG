from urllib.parse import urlparse

import yt_dlp

from src.media.podcast_document import (
    PodcastDocument
)

def detect_platform(
    url: str
) -> str:

    domain = (
        urlparse(url)
        .netloc
        .lower()
    )

    if "spotify" in domain:

        return "spotify"

    if "apple" in domain:

        return "apple"

    if "rss" in domain:

        return "rss"

    if "podbean" in domain:

        return "podbean"

    return "unknown"

def detect_platform(
    url: str
) -> str:

    domain = (
        urlparse(url)
        .netloc
        .lower()
    )

    if "spotify" in domain:

        return "spotify"

    if "apple" in domain:

        return "apple"

    if "rss" in domain:

        return "rss"

    if "podbean" in domain:

        return "podbean"

    return "unknown"

def extract_metadata(
    podcast_url: str
) -> dict:
    try:

        ydl_opts = {

            "quiet": True,

            "extract_flat": True
        }

        with yt_dlp.YoutubeDL(
            ydl_opts
        ) as ydl:

            info = (
                ydl.extract_info(
                    podcast_url,
                    download=False
                )
            )

            return {

                "title":
                    info.get(
                        "title",
                        ""
                    ),

                "description":
                    info.get(
                        "description",
                        ""
                    ),

                "duration":
                    info.get(
                        "duration",
                        0
                    )
            }

    except Exception:

        return {

            "title": "",

            "description": "",

            "duration": 0
        }

def create_podcast_document(
    celebrity_name: str,
    podcast_url: str
) -> PodcastDocument:

    metadata = extract_metadata(
        podcast_url
    )
    title = (
        metadata["title"]
        or
        podcast_url
    )

    return PodcastDocument(
        celebrity=celebrity_name,
        title=metadata["title"],
        url=podcast_url,
        description=metadata["description"],
        platform=detect_platform(podcast_url),
        duration=metadata["duration"]
    )