from src.media.youtube_search import (
    search_youtube_urls
)

from src.media.youtube_ingestor import (
    create_youtube_document
)

from src.storage.document_store import (
    save_youtube_documents
)


def ingest_youtube_videos(
    celebrity_name: str,
    max_videos: int = 10
):

    print(
        f"\nSearching YouTube videos "
        f"for {celebrity_name}"
    )

    youtube_results = (
        search_youtube_urls(
            celebrity_name,
            max_results=max_videos
        )
    )

    if not youtube_results:

        print(
            "No YouTube videos found."
        )

        return []

    youtube_documents = []

    for result in youtube_results:

        print(
            f"\nProcessing:"
            f"\n{result.title}"
        )

        try:

            document = (
                create_youtube_document(
                    celebrity_name,
                    result.url
                )
            )

            if not document.transcript:

                print(
                    "Skipping empty transcript"
                )

                continue

            youtube_documents.append(
                document
            )

            save_youtube_documents(
                celebrity_name,
                youtube_documents
            )

        except Exception as e:

            print(
                f"Failed: {e}"
            )

            continue

    save_youtube_documents(

        celebrity_name,

        youtube_documents
    )

    print(
        f"\nSaved "
        f"{len(youtube_documents)} "
        f"YouTube documents"
    )

    return youtube_documents


if __name__ == "__main__":
    ingest_youtube_videos()