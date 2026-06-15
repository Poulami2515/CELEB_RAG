from collections import Counter
from urllib.parse import urlparse

import json
from pathlib import Path
from datetime import datetime


BASE_STORAGE_DIR = Path(
    "storage/celebrities"
)


def get_celebrity_directory(
    celebrity_name: str
) -> Path:
    """
    Returns storage directory for a celebrity.
    """

    celebrity_folder = (
        celebrity_name
        .lower()
        .replace(" ", "_")
    )

    directory = (
        BASE_STORAGE_DIR /
        celebrity_folder
    )

    directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return directory


def save_documents(
    celebrity_name: str,
    documents: list
) -> None:
    """
    Save extracted documents to disk.
    """

    directory = get_celebrity_directory(
        celebrity_name
    )

    filepath = (
        directory /
        "documents.json"
    )

    serialized_documents = [
        document.model_dump()
        for document in documents
    ]

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            serialized_documents,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Saved {len(documents)} documents "
        f"to {filepath}"
    )

def save_media_documents(
    celebrity_name: str,
    documents: list,
    filename: str
) -> None:
    """
    Generic media document saver.

    Examples:
    ----------
    youtube_documents.json
    podcast_documents.json
    instagram_documents.json
    twitter_documents.json
    tiktok_documents.json
    """

    directory = get_celebrity_directory(
        celebrity_name
    )

    filepath = (
        directory /
        filename
    )

    serialized_documents = [
        document.model_dump()
        for document in documents
    ]

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            serialized_documents,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Saved {len(documents)} "
        f"documents to {filepath}"
    )


def load_media_documents(
    celebrity_name: str,
    filename: str
) -> list:
    """
    Generic media document loader.
    """

    directory = get_celebrity_directory(
        celebrity_name
    )

    filepath = (
        directory /
        filename
    )

    if not filepath.exists():

        return []

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_youtube_documents(
    celebrity_name: str,
    youtube_documents: list
) -> None:

    save_media_documents(
        celebrity_name,
        youtube_documents,
        "youtube_documents.json"
    )


def load_youtube_documents(
    celebrity_name: str
) -> list:

    return load_media_documents(
        celebrity_name,
        "youtube_documents.json"
    )


def save_podcast_documents(
    celebrity_name: str,
    podcast_documents: list
) -> None:

    save_media_documents(
        celebrity_name,
        podcast_documents,
        "podcast_documents.json"
    )


def load_podcast_documents(
    celebrity_name: str
) -> list:

    return load_media_documents(
        celebrity_name,
        "podcast_documents.json"
    )


def save_instagram_documents(
    celebrity_name: str,
    instagram_documents: list
) -> None:

    save_media_documents(
        celebrity_name,
        instagram_documents,
        "instagram_documents.json"
    )


def load_instagram_documents(
    celebrity_name: str
) -> list:

    return load_media_documents(
        celebrity_name,
        "instagram_documents.json"
    )


def save_twitter_documents(
    celebrity_name: str,
    twitter_documents: list
) -> None:

    save_media_documents(
        celebrity_name,
        twitter_documents,
        "twitter_documents.json"
    )


def load_twitter_documents(
    celebrity_name: str
) -> list:

    return load_media_documents(
        celebrity_name,
        "twitter_documents.json"
    )


def save_tiktok_documents(
    celebrity_name: str,
    tiktok_documents: list
) -> None:

    save_media_documents(
        celebrity_name,
        tiktok_documents,
        "tiktok_documents.json"
    )


def load_tiktok_documents(
    celebrity_name: str
) -> list:

    return load_media_documents(
        celebrity_name,
        "tiktok_documents.json"
    )


def load_documents(
    celebrity_name: str
) -> list:
    """
    Load stored documents.
    """

    directory = get_celebrity_directory(
        celebrity_name
    )

    filepath = (
        directory /
        "documents.json"
    )

    if not filepath.exists():

        print(
            f"No documents found "
            f"for {celebrity_name}"
        )

        return []

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_metadata(
    celebrity_name: str,
    document_count: int,
    source_urls: list[str]
) -> None:
    """
    Save metadata about ingestion.
    """

    directory = get_celebrity_directory(
        celebrity_name
    )

    filepath = (
        directory /
        "metadata.json"
    )

    domain_counter = Counter()

    for url in source_urls:
        try:
            domain = (
                urlparse(url)
                .netloc
                .lower()
            )
            if domain.startswith("www."):
                domain = domain[4:]
            if "wikipedia.org" in domain:
                domain = "wikipedia.org"
            if "imdb.com" in domain:
                domain = "imdb.com"
            if "bbc.com" in domain:
                domain = "bbc.com"
            domain_counter[domain] += 1
        except Exception:
            continue

    metadata = {
        "celebrity": celebrity_name,
        "document_count": document_count,
        "unique_domains": sorted(
            list(domain_counter.keys())
        ),
        "top_domains": dict(
            domain_counter.most_common(10)
        ),
        "source_count": len(
            source_urls
        ),
        "last_updated": (
            datetime.utcnow()
            .isoformat()
        ),
    }

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Saved metadata "
        f"to {filepath}"
    )


def load_metadata(
    celebrity_name: str
) -> dict:
    """
    Load metadata.json
    """

    directory = get_celebrity_directory(
        celebrity_name
    )

    filepath = (
        directory /
        "metadata.json"
    )

    if not filepath.exists():

        return {}

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def celebrity_exists(
    celebrity_name: str
) -> bool:
    """
    Check if celebrity has already
    been ingested.
    """

    directory = get_celebrity_directory(
        celebrity_name
    )

    filepath = (
        directory /
        "documents.json"
    )

    return filepath.exists()