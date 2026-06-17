# src/media/instagram_pipeline.py

from src.media.instagram_search import (
    search_instagram_urls
)

from src.media.instagram_ingestor import (
    create_instagram_documents
)

from src.storage.document_store import (
    save_instagram_documents
)


def ingest_instagram(
    celebrity_name: str,
    max_posts: int = 20
):
    """
    End-to-end Instagram ingestion.

    Search Instagram URLs
            ↓
    Create InstagramDocuments
            ↓
    Save to disk
    """

    print(
        f"\nStarting Instagram ingestion "
        f"for {celebrity_name}"
    )

    instagram_results = (
        search_instagram_urls(
            celebrity_name,
            max_results=max_posts
        )
    )

    print(
        f"Retrieved "
        f"{len(instagram_results)} "
        f"Instagram URLs"
    )

    instagram_documents = (
        create_instagram_documents(

            celebrity_name,

            instagram_results
        )
    )

    print(
        f"Created "
        f"{len(instagram_documents)} "
        f"Instagram documents"
    )

    save_instagram_documents(

        celebrity_name,

        instagram_documents
    )

    print(
        f"Instagram ingestion complete "
        f"for {celebrity_name}"
    )

    return instagram_documents


def print_instagram_summary(
    instagram_documents: list
):
    """
    Debug helper.
    """

    print()

    print(
        "=" * 60
    )

    print(
        "INSTAGRAM SUMMARY"
    )

    print(
        "=" * 60
    )

    print(
        f"Documents: "
        f"{len(instagram_documents)}"
    )

    profiles = 0
    reels = 0
    posts = 0

    for document in instagram_documents:

        if (
            document.content_type
            == "profile"
        ):
            profiles += 1

        elif (
            document.content_type
            == "reel"
        ):
            reels += 1

        elif (
            document.content_type
            == "post"
        ):
            posts += 1

    print(
        f"Profiles: {profiles}"
    )

    print(
        f"Reels: {reels}"
    )

    print(
        f"Posts: {posts}"
    )

    print(
        "=" * 60
    )