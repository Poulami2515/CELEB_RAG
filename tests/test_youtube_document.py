# tests/test_youtube_document.py

from src.media.youtube_ingestor import (
    create_youtube_document
)

url = (
    "https://www.youtube.com/watch?v=etRcxxm3Cco"
)

doc = create_youtube_document(
    "Rick Astley",
    url
)

print(doc.title)

print(
    len(doc.transcript)
)

print(
    doc.transcript[:2500]
)