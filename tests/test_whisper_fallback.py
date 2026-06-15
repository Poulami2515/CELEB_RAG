

from src.media.whisper_provider import (
    whisper_fallback
)

url = (
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
)

transcript = whisper_fallback(
    url
)

print(
    len(transcript)
)

print(
    transcript[:2500]
)