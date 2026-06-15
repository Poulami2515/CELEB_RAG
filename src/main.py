from src.ingestion.celebrity_ingestor import ingest_celebrity

from src.ingestion.celebrity_ingestor import (
    ingest_celebrity
)

from src.media.youtube_pipeline import (
    ingest_youtube_videos
)

def main():

    celebrity = (
        "Deepika Padukone"
    )

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

if __name__ == "__main__":
    main()