from src.media.youtube_ingestor import (
    create_youtube_document
)

from src.storage.document_store import (
    save_youtube_documents
)

url = (
    "https://www.youtube.com/watch?v="
    "dQw4w9WgXcQ"
)

doc = create_youtube_document(
    "Rick Astley",
    url
)

print(doc.title)

print(
    len(
        doc.transcript
    )
)

save_youtube_documents(

    "Rick Astley",

    [doc]
)