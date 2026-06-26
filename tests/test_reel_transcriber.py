from pathlib import Path
from unittest.mock import patch

from src.media.reel_transcriber import (
    transcribe_reel,
    transcribe_instagram_reels
)


# ============================================================
# Transcribe Single Reel
# ============================================================

def test_transcribe_single_reel(
    tmp_path
):

    post_directory = (
        tmp_path /
        "ABC123"
    )

    post_directory.mkdir()

    (
        post_directory /
        "reel.mp4"
    ).touch()

    with patch(

        "src.media.reel_transcriber."
        "transcribe_audio",

        return_value="Hello everyone."

    ) as mock_transcribe, patch(

        "src.media.reel_transcriber."
        "save_transcript"

    ) as mock_save_transcript, patch(

        "src.media.reel_transcriber."
        "update_transcript_metadata"

    ) as mock_update_metadata:

        transcribe_reel(
            post_directory
        )

        mock_transcribe.assert_called_once_with(
            str(post_directory / "reel.mp4")
        )

        mock_save_transcript.assert_called_once_with(

            post_directory,

            "Hello everyone."

        )

        mock_update_metadata.assert_called_once_with(

            post_directory

        )


# ============================================================
# Skip Already Transcribed Reel
# ============================================================

def test_skip_existing_transcript(
    tmp_path
):

    post_directory = (
        tmp_path /
        "ABC123"
    )

    post_directory.mkdir()

    (
        post_directory /
        "reel.mp4"
    ).touch()

    (
        post_directory /
        "transcript.txt"
    ).touch()

    with patch(

        "src.media.reel_transcriber."
        "transcribe_audio"

    ) as mock_transcribe:

        transcribe_reel(
            post_directory
        )

        mock_transcribe.assert_not_called()


# ============================================================
# Skip Directory Without Reel
# ============================================================

def test_skip_missing_reel(
    tmp_path
):

    post_directory = (
        tmp_path /
        "ABC123"
    )

    post_directory.mkdir()

    with patch(

        "src.media.reel_transcriber."
        "transcribe_audio"

    ) as mock_transcribe:

        transcribe_reel(
            post_directory
        )

        mock_transcribe.assert_not_called()


# ============================================================
# Whisper Exception
# ============================================================

def test_whisper_failure(
    tmp_path
):

    post_directory = (
        tmp_path /
        "ABC123"
    )

    post_directory.mkdir()

    (
        post_directory /
        "reel.mp4"
    ).touch()

    with patch(

        "src.media.reel_transcriber."
        "transcribe_audio",

        side_effect=RuntimeError(
            "Whisper failed."
        )

    ) as mock_transcribe:

        transcribe_reel(
            post_directory
        )

        mock_transcribe.assert_called_once()


# ============================================================
# Celebrity Pipeline
# ============================================================

def test_reel_pipeline(
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
            "reel.mp4"
        ).touch()

    with patch(

        "src.media.reel_transcriber."
        "get_instagram_media_directory"

    ) as mock_directory, patch(

        "src.media.reel_transcriber."
        "transcribe_audio",

        return_value="Transcript"

    ) as mock_transcribe, patch(

        "src.media.reel_transcriber."
        "save_transcript"

    ), patch(

        "src.media.reel_transcriber."
        "update_transcript_metadata"

    ):

        mock_directory.return_value = (
            media_directory
        )

        transcribe_instagram_reels(
            "Shah Rukh Khan"
        )

        assert (
            mock_transcribe.call_count
            ==
            2
        )
