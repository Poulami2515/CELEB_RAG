import os
import yt_dlp

from faster_whisper import (
    WhisperModel
)

def download_audio(
    youtube_url: str
) -> str:

    output_path = (
        "temp_audio.%(ext)s"
    )

    ydl_opts = {

        "format":
            "bestaudio/best",

        "outtmpl":
            output_path,

        "quiet":
            True
    }

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:

        ydl.download(
            [youtube_url]
        )

    for file in os.listdir():

        if file.startswith(
            "temp_audio"
        ):

            return file

    return ""

def transcribe_audio(
    audio_path: str
) -> str:

    device_configs = [
        ("cuda", "float16"),
        ("cpu", "int8"),
    ]

    last_error = None

    for device, compute_type in device_configs:

        try:

            model = WhisperModel(
                "base",
                device=device,
                compute_type=compute_type,
            )

            segments, info = (
                model.transcribe(
                    audio_path
                )
            )

            return " ".join(

                segment.text

                for segment in segments

            )

        except RuntimeError as error:

            last_error = error

            if device == "cuda":

                print(
                    f"Whisper GPU failed: {error}. "
                    "Falling back to CPU."
                )

                continue

            raise

    if last_error:

        raise last_error

    return ""

def whisper_fallback(
    youtube_url: str
) -> str:

    audio_path = (
        download_audio(
            youtube_url
        )
    )

    if not audio_path:

        return ""

    transcript = (
        transcribe_audio(
            audio_path
        )
    )

    os.remove(
        audio_path
    )

    return transcript
