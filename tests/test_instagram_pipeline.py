# tests/test_instagram_pipeline.py

from src.media.instagram_pipeline import (
    ingest_instagram,
    print_instagram_summary
)

documents = ingest_instagram(
    "Shah Rukh Khan"
)

print_instagram_summary(
    documents
)