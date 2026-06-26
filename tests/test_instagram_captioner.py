from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from src.media.instagram_captioner import (

    caption_instagram_post,

    caption_instagram_media

)


# ============================================================
# Caption Single Image
# ============================================================

def test_caption_single_post(
    tmp_path
):

    post_directory = (
        tmp_path /
        "ABC123"
    )

    post_directory.mkdir()

    (
        post_directory /
        "image.jpg"
    ).touch()

    mock_vlm = MagicMock()

    mock_vlm.caption_image.return_value = (

        "Shah Rukh Khan wearing "
        "a black suit."

    )

    with patch(

        "src.media.instagram_captioner."
        "save_caption"

    ) as mock_save_caption, patch(

        "src.media.instagram_captioner."
        "update_metadata"

    ) as mock_update_metadata:

        caption_instagram_post(

            mock_vlm,

            post_directory

        )

        mock_vlm.caption_image.assert_called_once()

        mock_save_caption.assert_called_once()

        mock_update_metadata.assert_called_once()


# ============================================================
# Skip Already Captioned Image
# ============================================================

def test_skip_captioned_post(
    tmp_path
):

    post_directory = (
        tmp_path /
        "ABC123"
    )

    post_directory.mkdir()

    (
        post_directory /
        "image.jpg"
    ).touch()

    (
        post_directory /
        "vlm_caption.txt"
    ).touch()

    mock_vlm = MagicMock()

    caption_instagram_post(

        mock_vlm,

        post_directory

    )

    mock_vlm.caption_image.assert_not_called()


# ============================================================
# Skip Non Image
# ============================================================

def test_skip_without_image(
    tmp_path
):

    post_directory = (
        tmp_path /
        "ABC123"
    )

    post_directory.mkdir()

    mock_vlm = MagicMock()

    caption_instagram_post(

        mock_vlm,

        post_directory

    )

    mock_vlm.caption_image.assert_not_called()


# ============================================================
# Pipeline
# ============================================================

@patch(

    "src.media.instagram_captioner."
    "OpenRouterVisionLanguageModel"

)

def test_caption_pipeline(

    mock_vlm_class,

    tmp_path

):

    media_directory = (
        tmp_path /
        "instagram_media"
    )

    media_directory.mkdir()

    for shortcode in [

        "ABC123",

        "XYZ789"

    ]:

        post = (
            media_directory /
            shortcode
        )

        post.mkdir()

        (
            post /
            "image.jpg"
        ).touch()

    mock_vlm = MagicMock()

    mock_vlm.caption_image.return_value = (

        "caption"

    )

    mock_vlm_class.return_value = (

        mock_vlm

    )

    with patch(

        "src.media.instagram_captioner."
        "get_instagram_media_directory"

    ) as mock_directory, patch(

        "src.media.instagram_captioner."
        "save_caption"

    ), patch(

        "src.media.instagram_captioner."
        "update_metadata"

    ):

        mock_directory.return_value = (

            media_directory

        )

        caption_instagram_media(

            "Shah Rukh Khan"

        )

        assert (

            mock_vlm.caption_image.call_count

            ==

            2

        )


# ============================================================
# VLM Failure
# ============================================================

def test_vlm_exception(
    tmp_path
):

    post_directory = (
        tmp_path /
        "ABC123"
    )

    post_directory.mkdir()

    (
        post_directory /
        "image.jpg"
    ).touch()

    mock_vlm = MagicMock()

    mock_vlm.caption_image.side_effect = (

        RuntimeError(
            "OpenRouter Error"
        )

    )

    caption_instagram_post(

        mock_vlm,

        post_directory

    )

    mock_vlm.caption_image.assert_called_once()