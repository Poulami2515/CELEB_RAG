# tests/test_instagram_ingestor.py

from src.media.instagram_search import (
    search_instagram_urls
)

from src.media.instagram_ingestor import (
    create_instagram_documents,
    print_instagram_documents
)


results = search_instagram_urls(
    "Shah Rukh Khan"
)

documents = (
    create_instagram_documents(

        "Shah Rukh Khan",

        results
    )
)

print_instagram_documents(
    documents
)