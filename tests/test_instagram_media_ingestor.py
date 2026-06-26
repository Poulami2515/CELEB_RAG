import json
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

from src.media.instagram_media_ingestor import (
    extract_username_from_url,
    extract_hashtags,
    extract_mentions,
    create_post_directory,
    create_instagram_media_document,
    ingest_instagram_media
)


# ============================================================
# Username Extraction
# ============================================================

def test_extract_username():

    url = "https://www.instagram.com/iamsrk/"

    assert (
        extract_username_from_url(url)
        == "iamsrk"
    )


# ============================================================
# Hashtag Extraction
# ============================================================

def test_extract_hashtags():

    caption = (
        "King Khan #bollywood "
        "#srk #pathaan"
    )

    hashtags = extract_hashtags(
        caption
    )

    assert hashtags == [

        "#bollywood",

        "#srk",

        "#pathaan"

    ]


# ============================================================
# Mention Extraction
# ============================================================

def test_extract_mentions():

    caption = (
        "With @iamsrk "
        "@gaurikhan"
    )

    mentions = extract_mentions(
        caption
    )

    assert mentions == [

        "@iamsrk",

        "@gaurikhan"

    ]


# ============================================================
# Directory Creation
# ============================================================

def test_create_post_directory(
    tmp_path
):

    with patch(

        "src.media.instagram_media_ingestor."
        "get_instagram_media_directory"

    ) as mock_directory:

        mock_directory.return_value = tmp_path

        directory = create_post_directory(

            "Shah Rukh Khan",

            "ABC123"

        )

        assert directory.exists()

        assert directory.name == "ABC123"


# ============================================================
# Media Document Creation
# ============================================================

def test_create_media_document(
    tmp_path
):

    post = tmp_path / "ABC123"

    post.mkdir()

    metadata = {

        "celebrity":
            "Shah Rukh Khan",

        "username":
            "iamsrk",

        "shortcode":
            "ABC123",

        "post_url":
            "https://instagram.com/p/ABC123",

        "media_type":
            "image",

        "instagram_caption":
            "Hello",

        "hashtags":
            ["#srk"],

        "mentions":
            ["@gaurikhan"],

        "likes":
            10,

        "comments":
            2,

        "timestamp":
            "2025",

        "downloaded":
            True,

        "vlm_caption_generated":
            False,

        "transcript_generated":
            False,

        "embedding_ready":
            False

    }

    with open(

        post / "metadata.json",

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            metadata,

            file

        )

    (
        post /
        "image.jpg"
    ).touch()

    document = create_instagram_media_document(

        "Shah Rukh Khan",

        post

    )

    assert (

        document.shortcode

        ==

        "ABC123"

    )

    assert (

        document.media_type

        ==

        "image"

    )


# ============================================================
# Pipeline
# ============================================================

@patch(

    "src.media.instagram_media_ingestor."
    "download_instagram_media"

)

def test_ingest_instagram_media(

    mock_download

):

    mock_download.return_value = [

        {

            "media_directory":

            "/tmp/ABC123"

        }

    ]

    with patch(

        "src.media.instagram_media_ingestor."
        "create_instagram_media_document"

    ) as mock_document:

        mock_document.return_value = MagicMock()

        documents = ingest_instagram_media(

            "Shah Rukh Khan"

        )

        assert len(documents) == 1

        mock_download.assert_called_once()

        mock_document.assert_called_once()