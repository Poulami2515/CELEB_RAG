from src.ingestion.celebrity_ingestor import ingest_celebrity

from src.ingestion.celebrity_ingestor import (
    ingest_celebrity
)

from src.media.youtube_pipeline import (
    ingest_youtube_videos
)

from src.media.podcast_pipeline import (
    ingest_podcasts
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

    # ----------------------------------
    # PODCASTS
    # ----------------------------------

    print(
        "\n[3/3] Podcast Ingestion"
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
        )
    }


def main():

    celebrity = (
        "Shah Rukh Khan"
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