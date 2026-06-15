# tests/test_audio_download.py

from src.media.whisper_provider import (
    download_audio
)

url = (
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
)

audio_file = download_audio(url)

print(audio_file)