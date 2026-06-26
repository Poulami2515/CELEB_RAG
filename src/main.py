from src.ingestion.celebrity_ingestor import (
    ingest_celebrity
)

from src.media.youtube_pipeline import (
    ingest_youtube_videos
)

from src.media.podcast_pipeline import (
    ingest_podcasts
)

from src.media.instagram_pipeline import (
    ingest_instagram
)

from src.media.instagram_media_pipeline import (
    process_instagram_media
)


def ingest_all_sources(
    celebrity: str,
):

    print(
        "\n=== WEB INGESTION ===\n"
    )

    documents = (
        ingest_celebrity(
            celebrity
        )
    )

    print(
        f"Ingested "
        f"{len(documents)} "
        f"web documents"
    )

    print(
        "\n=== YOUTUBE INGESTION ===\n"
    )

    youtube_documents = (
        ingest_youtube_videos(
            celebrity,
            max_videos=5
        )
    )

    print(
        f"Ingested "
        f"{len(youtube_documents)} "
        f"YouTube documents"
    )

    print(
        "\n=== PODCAST INGESTION ===\n"
    )

    podcast_documents = (
        ingest_podcasts(
            celebrity
        )
    )

    print(
        f"Podcast Documents: "
        f"{len(podcast_documents)}"
    )

    print(
        "\n=== INSTAGRAM INGESTION ===\n"
    )

    instagram_documents = (
        ingest_instagram(
            celebrity,
            max_posts=10
        )
    )

    print(
        f"Instagram Documents: "
        f"{len(instagram_documents)}"
    )

    print(
        "\n=== INSTAGRAM MEDIA PROCESSING ===\n"
    )

    process_instagram_media(
        celebrity
    )

    print(
        "\nFinished ingestion."
    )

    return {

        "web": len(
            documents
        ),

        "youtube": len(
            youtube_documents
        ),

        "podcasts": len(
            podcast_documents
        ),

        "instagram": len(
            instagram_documents
        ),
    }


def main():

    celebrity = (
        "Katrina Kaif"
    )

    stats = (
        ingest_all_sources(
            celebrity
        )
    )

    print(
        "\nFinal Stats:"
    )

    print(stats)


if __name__ == "__main__":
    main()
