from src.media.podcast_search import (
    search_podcast_urls
)

from src.media.podcast_ingestor import (
    create_podcast_document
)

from src.storage.document_store import (
    save_podcast_documents
)

def ingest_podcasts(
    celebrity_name: str,
    max_podcasts: int = 10
):
    podcast_results = (
        search_podcast_urls(
            celebrity_name,
            max_results=max_podcasts
        )
    )

    podcast_documents = []

    for result in podcast_results:

        try:

            document = (
                create_podcast_document(

                    celebrity_name,

                    result.url
                )
            )

            podcast_documents.append(
                document
            )

        except Exception as e:

            print(
                f"Failed: {e}"
            )

    save_podcast_documents(

        celebrity_name,

        podcast_documents
    )

    return podcast_documents