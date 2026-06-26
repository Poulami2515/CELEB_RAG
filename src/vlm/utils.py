from pathlib import Path
import base64
import json
import mimetypes


# ==========================================================
# Image Encoding
# ==========================================================

def image_to_base64(
    image_path: Path
) -> str:
    """
    Convert an image into a Base64 string.
    """

    with open(
        image_path,
        "rb"
    ) as file:

        return base64.b64encode(
            file.read()
        ).decode(
            "utf-8"
        )


# ==========================================================
# MIME Type
# ==========================================================

def detect_mime_type(
    image_path: Path
) -> str:
    """
    Detect image MIME type.
    """

    mime_type = mimetypes.guess_type(
        image_path
    )[0]

    if mime_type is None:

        mime_type = "image/jpeg"

    return mime_type


# ==========================================================
# Caption File
# ==========================================================

def save_caption(
    post_directory: Path,
    caption: str
):

    caption_path = (
        post_directory /
        "vlm_caption.txt"
    )

    with open(

        caption_path,

        "w",

        encoding="utf-8"

    ) as file:

        file.write(
            caption
        )


def load_caption(
    post_directory: Path
) -> str:

    caption_path = (
        post_directory /
        "vlm_caption.txt"
    )

    if not caption_path.exists():

        return ""

    with open(

        caption_path,

        "r",

        encoding="utf-8"

    ) as file:

        return file.read().strip()


# ==========================================================
# Metadata
# ==========================================================

def load_metadata(
    post_directory: Path
) -> dict:

    metadata_path = (
        post_directory /
        "metadata.json"
    )

    with open(

        metadata_path,

        "r",

        encoding="utf-8"

    ) as file:

        return json.load(
            file
        )


def save_metadata(
    post_directory: Path,
    metadata: dict
):

    metadata_path = (
        post_directory /
        "metadata.json"
    )

    with open(

        metadata_path,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            metadata,

            file,

            indent=4,

            ensure_ascii=False

        )


def update_metadata(
    post_directory: Path,
    **kwargs
):

    metadata = load_metadata(
        post_directory
    )

    metadata.update(
        kwargs
    )

    save_metadata(

        post_directory,

        metadata

    )


# ==========================================================
# File Checks
# ==========================================================

def image_exists(
    post_directory: Path
) -> bool:

    return (

        (
            post_directory /
            "image.jpg"
        ).exists()

    )


def caption_exists(
    post_directory: Path
) -> bool:

    return (

        (
            post_directory /
            "vlm_caption.txt"
        ).exists()

    )


# ==========================================================
# Dataset Traversal
# ==========================================================

def collect_images(
    instagram_media_directory: Path
) -> list[Path]:
    """
    Collect all image.jpg files
    recursively.
    """

    return list(

        instagram_media_directory.rglob(
            "image.jpg"
        )

    )