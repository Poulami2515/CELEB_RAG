from src.media.instagram_media_ingestor import (
    ingest_instagram_media
)

from src.media.instagram_captioner import (
    caption_instagram_media
)

from src.media.reel_transcriber import (
    transcribe_instagram_reels
)


# ==========================================================
# Instagram Media Pipeline
# ==========================================================

def process_instagram_media(
    celebrity_name: str
):
    """
    Complete Instagram media pipeline.

    Stages
    ------

    1. Download media
    2. Caption images
    3. Transcribe reels
    """

    print()

    print("=" * 60)
    print("INSTAGRAM MEDIA PIPELINE")
    print("=" * 60)

    print()

    print(
        "Downloading Instagram media..."
    )

    ingest_instagram_media(
        celebrity_name
    )

    print()

    print(
        "Generating image captions..."
    )

    caption_instagram_media(
        celebrity_name
    )

    print()

    print(
        "Transcribing reels..."
    )

    transcribe_instagram_reels(
        celebrity_name
    )

    print()

    print("=" * 60)
    print("INSTAGRAM MEDIA COMPLETE")
    print("=" * 60)
    print()