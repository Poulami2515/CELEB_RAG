# tests/test_podcast_pipeline.py

from src.media.podcast_pipeline import (
    ingest_podcasts
)

documents = ingest_podcasts(
    "Shah Rukh Khan"
)

print(
    f"Retrieved "
    f"{len(documents)} podcasts"
)