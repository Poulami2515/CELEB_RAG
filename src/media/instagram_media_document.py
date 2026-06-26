from typing import Optional

from pydantic import BaseModel


class InstagramMediaDocument(BaseModel):
    """
    Represents one downloaded Instagram
    media item (image or reel).

    Every document corresponds to one
    Instagram shortcode directory.
    """

    # ----------------------------------
    # Identity
    # ----------------------------------

    celebrity: str

    source_type: str = "instagram_media"

    username: str

    shortcode: str

    media_type: str
    # image | reel

    # ----------------------------------
    # Instagram Information
    # ----------------------------------

    post_url: str

    instagram_caption: str

    hashtags: list[str] = []

    mentions: list[str] = []

    likes: int = 0

    comments: int = 0

    timestamp: str

    # ----------------------------------
    # Local Storage
    # ----------------------------------

    media_directory: str
    # storage/.../instagram_media/<shortcode>/

    media_filename: str
    # image.jpg
    # reel.mp4

    thumbnail_filename: Optional[str] = None

    audio_filename: Optional[str] = None

    # ----------------------------------
    # AI Generated Content
    # ----------------------------------

    vlm_caption: Optional[str] = None

    transcript: Optional[str] = None

    transcript_language: Optional[str] = None

    # ----------------------------------
    # Processing Status
    # ----------------------------------

    downloaded: bool = True

    caption_generated: bool = False

    transcript_generated: bool = False

    embedding_ready: bool = False

    # ----------------------------------
    # Future Extension
    # ----------------------------------

    metadata: dict = {}