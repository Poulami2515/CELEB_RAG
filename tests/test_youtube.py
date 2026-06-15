from src.media.youtube_ingestor import (
    create_youtube_document
)


url = (
    "https://www.youtube.com/watch?v="
    "etRcxxm3Cco"
)

doc = create_youtube_document(
    "Shah Rukh Khan",
    url
)

print(doc)
print(
    len(doc.transcript)
)
print(
    doc.transcript[:500]
)

from youtube_transcript_api import (
    YouTubeTranscriptApi
)

video_id = "dQw4w9WgXcQ"

api = YouTubeTranscriptApi()

transcript = api.fetch(video_id)

print(type(transcript))

print(transcript[:500])