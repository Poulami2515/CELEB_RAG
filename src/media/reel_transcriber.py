from pathlib import Path

from src.media.whisper_provider import transcribe_audio

from src.storage.document_store import (
    get_celebrity_directory
)

from src.vlm.utils import (
    load_metadata,
    save_metadata
)


# ==========================================================
# Paths
# ==========================================================

def get_instagram_media_directory(
    celebrity_name: str
) -> Path:

    return (
        get_celebrity_directory(
            celebrity_name
        )
        /
        "instagram_media"
    )


# ==========================================================
# Helper Functions
# ==========================================================

def reel_exists(
    post_directory: Path
) -> bool:

    return (
        post_directory /
        "reel.mp4"
    ).exists()


def transcript_exists(
    post_directory: Path
) -> bool:

    return (
        post_directory /
        "transcript.txt"
    ).exists()


def save_transcript(
    post_directory: Path,
    transcript: str
):

    transcript_path = (
        post_directory /
        "transcript.txt"
    )

    with open(

        transcript_path,

        "w",

        encoding="utf-8"

    ) as file:

        file.write(
            transcript
        )


def update_transcript_metadata(
    post_directory: Path
):

    metadata = load_metadata(
        post_directory
    )

    metadata[
        "transcript_generated"
    ] = True

    save_metadata(
        post_directory,
        metadata
    )


# ==========================================================
# Single Reel
# ==========================================================

def transcribe_reel(
    post_directory: Path
):

    if not reel_exists(
        post_directory
    ):
        return

    if transcript_exists(
        post_directory
    ):

        print(
            f"Skipping "
            f"{post_directory.name}"
        )

        return

    reel_path = (
        post_directory /
        "reel.mp4"
    )

    try:

        transcript = transcribe_audio(
            str(reel_path)
        )

        save_transcript(

            post_directory,

            transcript

        )

        update_transcript_metadata(
            post_directory
        )

        print(
            f"Transcribed "
            f"{post_directory.name}"
        )

    except Exception as e:

        print(
            f"Failed "
            f"{post_directory.name}: "
            f"{e}"
        )


# ==========================================================
# Celebrity
# ==========================================================

def transcribe_instagram_reels(
    celebrity_name: str
):

    media_directory = (
        get_instagram_media_directory(
            celebrity_name
        )
    )

    if not media_directory.exists():

        print(
            "Instagram media "
            "not found."
        )

        return

    post_directories = sorted(

        [

            path

            for path

            in media_directory.iterdir()

            if path.is_dir()

        ]

    )

    print()

    print(
        f"Processing "
        f"{len(post_directories)} "
        f"Instagram posts..."
    )

    print()

    for post_directory in post_directories:

        transcribe_reel(
            post_directory
        )

    print()

    print(
        "Instagram reel "
        "transcription complete."
    )