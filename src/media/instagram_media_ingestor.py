import json
import re
import shutil

from pathlib import Path
from urllib.parse import urlparse

import instaloader

from src.media.instagram_media_document import (
    InstagramMediaDocument
)

from src.storage.document_store import (
    load_instagram_documents,
    get_celebrity_directory
)

MAX_REELS = 5

def extract_username_from_url(
    url: str
) -> str:
    """
    Extract Instagram username from an Instagram URL.

    Supported URLs
    --------------
    https://www.instagram.com/iamsrk/
    https://www.instagram.com/iamsrk/reel/ABC123/
    https://www.instagram.com/iamsrk/p/XYZ789/
    https://instagram.com/iamsrk
    """

    parsed_url = urlparse(url)

    path_parts = [

        part

        for part

        in parsed_url.path.split("/")

        if part
    ]

    if not path_parts:

        raise ValueError(
            f"Invalid Instagram URL: {url}"
        )

    username = path_parts[0]

    reserved_paths = {

        "p",

        "reel",

        "tv",

        "stories",

        "explore",

        "accounts",

        "directory"
    }

    if username.lower() in reserved_paths:

        raise ValueError(
            f"Cannot extract username from: {url}"
        )

    return username




def extract_hashtags(
    caption: str
) -> list[str]:
    """
    Extract hashtags from an Instagram caption.

    Examples
    --------
    #Pathaan
    #SRK
    #King

    Returns
    -------
    [
        "#pathaan",
        "#srk",
        "#king"
    ]
    """

    if not caption:

        return []

    hashtags = re.findall(

        r"#[A-Za-z0-9_]+",

        caption
    )

    hashtags = [

        hashtag.lower()

        for hashtag

        in hashtags
    ]

    hashtags = list(

        dict.fromkeys(
            hashtags
        )
    )

    return hashtags




def extract_mentions(
    caption: str
) -> list[str]:
    """
    Extract Instagram mentions from a caption.

    Examples
    --------
    @iamsrk
    @deepikapadukone
    @virat.kohli

    Returns
    -------
    [
        "@iamsrk",
        "@deepikapadukone",
        "@virat.kohli"
    ]
    """

    if not caption:

        return []

    mentions = re.findall(

        r"@[A-Za-z0-9._]+",

        caption
    )

    mentions = [

        mention.lower()

        for mention

        in mentions
    ]

    mentions = list(

        dict.fromkeys(
            mentions
        )
    )

    return mentions


def get_instagram_media_directory(
    celebrity_name: str
) -> Path:
    """
    Return the Instagram media directory for a celebrity.

    Creates the directory if it does not already exist.

    Example
    -------
    storage/
        celebrities/
            shah_rukh_khan/
                instagram_media/
    """

    celebrity_directory = (
        get_celebrity_directory(
            celebrity_name
        )
    )

    media_directory = (
        celebrity_directory /
        "instagram_media"
    )

    media_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return media_directory




def create_post_directory(
    celebrity_name: str,
    shortcode: str
) -> Path:
    """
    Create a directory for a single Instagram post.

    Directory structure
    -------------------
    storage/
        celebrities/
            <celebrity>/
                instagram_media/
                    <shortcode>/

    Returns
    -------
    pathlib.Path
        Path to the shortcode directory.
    """

    media_directory = (
        get_instagram_media_directory(
            celebrity_name
        )
    )

    post_directory = (
        media_directory /
        shortcode
    )

    post_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return post_directory


def load_official_instagram_profile(
    celebrity_name: str
) -> dict:
    """
    Load the official Instagram profile selected
    during instagram_pipeline.py.

    Returns
    -------
    {
        "username": "...",
        "url": "...",
        "title": "...",
        "content": "..."
    }
    """

    documents = load_instagram_documents(
        celebrity_name
    )

    if not documents:

        raise ValueError(
            f"No Instagram documents found for "
            f"{celebrity_name}"
        )

    for document in documents:

        if (
            document.get("content_type")
            == "profile"
        ):

            username = extract_username_from_url(
                document["url"]
            )

            return {

                "username": username,

                "url": document["url"],

                "title": document.get(
                    "title",
                    ""
                ),

                "content": document.get(
                    "content",
                    ""
                )
            }

    raise ValueError(
        f"Official Instagram profile not found "
        f"for {celebrity_name}"
    )





def create_instaloader() -> instaloader.Instaloader:
    """
    Create and configure an Instaloader instance.

    Returns
    -------
    instaloader.Instaloader
        Configured Instaloader object.
    """

    loader = instaloader.Instaloader(

        # ----------------------------
        # Download Settings
        # ----------------------------

        download_pictures=True,

        download_videos=True,

        download_video_thumbnails=False,

        download_geotags=False,

        download_comments=False,

        save_metadata=False,

        compress_json=False,

        post_metadata_txt_pattern="",

        dirname_pattern="{target}",

        filename_pattern="{shortcode}",

        max_connection_attempts=3,

        request_timeout=30
    )

    return loader



def save_post_metadata(
    post_directory: Path,
    post
) -> Path:
    """
    Save metadata for one Instagram post.

    Creates

        metadata.json

    inside the shortcode directory.

    Parameters
    ----------
    post_directory : Path
        Directory corresponding to one Instagram shortcode.

    post : instaloader.Post
        Instagram post object.

    Returns
    -------
    Path
        Path to metadata.json.
    """

    metadata = {

        # -------------------------
        # Identity
        # -------------------------

        "shortcode": post.shortcode,

        "post_url":
        f"https://www.instagram.com/p/{post.shortcode}/",

        "media_type":
        "reel" if post.is_video else "image",

        # -------------------------
        # Author
        # -------------------------

        "username":
        post.owner_username,

        # -------------------------
        # Instagram Metadata
        # -------------------------

        "instagram_caption":
        post.caption or "",

        "hashtags":
        extract_hashtags(
            post.caption or ""
        ),

        "mentions":
        extract_mentions(
            post.caption or ""
        ),

        "likes":
        post.likes,

        "comments":
        post.comments,

        "timestamp":
        post.date_utc.isoformat(),

        "is_video":
        post.is_video,

        # -------------------------
        # Processing Status
        # -------------------------

        "downloaded": True,

        "vlm_caption_generated": False,

        "transcript_generated": False,

        "embedding_ready": False

    }

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

    return metadata_path


def download_instagram_media(
    celebrity_name: str,
    max_reels: int = MAX_REELS
) -> list[InstagramMediaDocument]:
    """
    Download Instagram media from the
    official profile.

    Downloads
    ----------
    • All image posts
    • First max_reels reels

    Saves
    -----
    metadata.json inside every
    shortcode directory.

    Returns
    -------
    list[InstagramMediaDocument]
        Information about every
        downloaded media item.
    """

    profile = load_official_instagram_profile(
        celebrity_name
    )

    username = profile["username"]

    print(
        f"Downloading Instagram media "
        f"from @{username}"
    )

    loader = create_instaloader()

    instagram_profile = (
        instaloader.Profile.from_username(
            loader.context,
            username
        )
    )

    downloaded_media = []

    reel_count = 0

    for post in instagram_profile.get_posts():

        # ---------------------------------
        # Limit reels
        # ---------------------------------

        if post.is_video:

            if reel_count >= max_reels:
                continue

            reel_count += 1

        # ---------------------------------
        # Create shortcode directory
        # ---------------------------------

        post_directory = (
            create_post_directory(
                celebrity_name,
                post.shortcode
            )
        )

        metadata_file = (
            post_directory /
            "metadata.json"
        )

        # ---------------------------------
        # Skip already downloaded posts
        # ---------------------------------

        if metadata_file.exists():

            print(
                f"Skipping "
                f"{post.shortcode}"
            )

            continue

        print(
            f"Downloading "
            f"{post.shortcode}"
        )

        # ---------------------------------
        # Download post
        # ---------------------------------

        try:
            loader.download_post(
            post,
            target=str(
                post_directory
            )
        )
        except Exception as e:
            print(
                f"Failed to download post: "
                f"{e}"
            )
            continue

        media_path = None

        # ---------------------------------
        # Rename downloaded media
        # ---------------------------------

        for file in post_directory.iterdir():

            suffix = file.suffix.lower()

            if (file.stem == post.shortcode and suffix in {
                ".jpg",
                ".jpeg",
                ".png"
            }):

                media_path = (
                    post_directory /
                    "image.jpg"
                )

                shutil.move(
                    file,
                    media_path
                )

                break

            elif suffix == ".mp4":

                media_path = (
                    post_directory /
                    "reel.mp4"
                )

                shutil.move(
                    file,
                    media_path
                )

                break

        # ---------------------------------
        # Save metadata.json
        # ---------------------------------

        save_post_metadata(
            post_directory,
            post
        )

        downloaded_media.append(

            {

                "shortcode":
                    post.shortcode,

                "media_directory":
                    str(post_directory),

                "media_path":
                    str(media_path),

                "media_type":
                    "reel"
                    if post.is_video
                    else "image",

                "username":
                    username
            }

        )

    print()

    print(
        f"Downloaded "
        f"{len(downloaded_media)} "
        f"media items."
    )

    return downloaded_media



def create_instagram_media_document(
    celebrity_name: str,
    media_directory: Path
) -> InstagramMediaDocument:
    """
    Create an InstagramMediaDocument from a
    downloaded Instagram post directory.

    Expected directory structure
    ----------------------------

    <shortcode>/

        metadata.json

        image.jpg
            OR
        reel.mp4

        vlm_caption.txt      (optional)

        transcript.txt       (optional)
    """

    metadata_file = (
        media_directory /
        "metadata.json"
    )

    if not metadata_file.exists():

        raise FileNotFoundError(
            f"{metadata_file} not found."
        )

    with open(
        metadata_file,
        "r",
        encoding="utf-8"
    ) as file:

        metadata = json.load(file)

    # ---------------------------------
    # Media filename
    # ---------------------------------

    media_filename = ""

    if (
        media_directory /
        "image.jpg"
    ).exists():

        media_filename = "image.jpg"

    elif (
        media_directory /
        "reel.mp4"
    ).exists():

        media_filename = "reel.mp4"

    # ---------------------------------
    # Optional files
    # ---------------------------------

    thumbnail = None

    if (
        media_directory /
        "thumbnail.jpg"
    ).exists():

        thumbnail = "thumbnail.jpg"

    audio = None

    if (
        media_directory /
        "audio.wav"
    ).exists():

        audio = "audio.wav"

    # ---------------------------------
    # Optional AI outputs
    # ---------------------------------

    vlm_caption = None

    caption_file = (
        media_directory /
        "vlm_caption.txt"
    )

    if caption_file.exists():

        with open(
            caption_file,
            "r",
            encoding="utf-8"
        ) as file:

            vlm_caption = (
                file.read()
                .strip()
            )

    transcript = None

    transcript_file = (
        media_directory /
        "transcript.txt"
    )

    if transcript_file.exists():

        with open(
            transcript_file,
            "r",
            encoding="utf-8"
        ) as file:

            transcript = (
                file.read()
                .strip()
            )

    # ---------------------------------
    # Build document
    # ---------------------------------

    document = InstagramMediaDocument(

        celebrity=celebrity_name,

        username=metadata["username"],

        shortcode=metadata["shortcode"],

        media_type=metadata["media_type"],

        post_url=metadata["post_url"],

        instagram_caption=metadata[
            "instagram_caption"
        ],

        hashtags=metadata[
            "hashtags"
        ],

        mentions=metadata[
            "mentions"
        ],

        likes=metadata[
            "likes"
        ],

        comments=metadata[
            "comments"
        ],

        timestamp=metadata[
            "timestamp"
        ],

        media_directory=str(
            media_directory
        ),

        media_filename=media_filename,

        thumbnail_filename=thumbnail,

        audio_filename=audio,

        vlm_caption=vlm_caption,

        transcript=transcript,

        downloaded=metadata[
            "downloaded"
        ],

        caption_generated=metadata[
            "vlm_caption_generated"
        ],

        transcript_generated=metadata[
            "transcript_generated"
        ],

        embedding_ready=metadata[
            "embedding_ready"
        ]

    )

    return document


def ingest_instagram_media(
    celebrity_name: str,
    max_reels: int = MAX_REELS
) -> list[InstagramMediaDocument]:

    downloaded = download_instagram_media(
        celebrity_name,
        max_reels
    )

    documents = []

    for item in downloaded:

        document = create_instagram_media_document(
            celebrity_name,
            Path(item["media_directory"])
        )

        documents.append(document)

    return documents