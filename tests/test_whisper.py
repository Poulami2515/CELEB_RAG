# tests/test_whisper.py

from src.media.whisper_provider import (
    download_audio,
    transcribe_audio
)

url = (
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
)

audio_file = download_audio(url)

print("Downloaded:", audio_file)

transcript = transcribe_audio(
    audio_file
)

print(
    transcript[:1000]
)