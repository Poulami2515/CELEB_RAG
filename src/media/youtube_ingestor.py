from urllib.parse import (
    urlparse,
    parse_qs
)

#from pytube import YouTube
import yt_dlp

from youtube_transcript_api import (
    YouTubeTranscriptApi
)

from src.models.youtube_document import (
    YouTubeDocument
)
from src.storage.document_store import (
    save_youtube_documents
)

from src.media.whisper_provider import (
    whisper_fallback
)

from src.storage.failure_store import (
    save_failed_url
)

def extract_video_id(
    youtube_url: str
) -> str:

    parsed = urlparse(
        youtube_url
    )

    if parsed.hostname == "youtu.be":

        return parsed.path[1:]

    return parse_qs(
        parsed.query
    ).get(
        "v",
        [None]
    )[0]


def get_video_title(
    youtube_url: str
) -> str:

    try:

        ydl_opts = {
            "quiet": True
        }

        with yt_dlp.YoutubeDL(
            ydl_opts
        ) as ydl:

            info = ydl.extract_info(
                youtube_url,
                download=False
            )

            return info.get(
                "title",
                ""
            )

    except Exception as e:

        print(
            f"Title Error: {e}"
        )

        return ""


def get_transcript(
    video_id: str,
    youtube_url: str,
) -> str:

    try:

        api = (
            YouTubeTranscriptApi()
        )

        transcript = (
            api.fetch(
                video_id
            )
        )

        return " ".join(

            snippet.text

            for snippet in transcript

        )

    except Exception as e:

        print(
            f"Transcript API failed: {e}"
        )

        save_failed_url(

            youtube_url,

            video_id,

            str(e)
        )

        print(
            "Trying Whisper fallback..."
        )

        transcript = (
            whisper_fallback(
                youtube_url
            )
        )

        return transcript


def create_youtube_document(
    celebrity_name: str,
    youtube_url: str
) -> YouTubeDocument:

    video_id = extract_video_id(
        youtube_url
    )
    title = get_video_title(
        youtube_url
    )
    transcript = get_transcript(
        video_id,
        youtube_url,
    )
    youtube_url = youtube_url.strip()

    return YouTubeDocument(

        celebrity=celebrity_name,

        source_type="youtube",

        video_id=video_id,

        title=title,

        url=youtube_url,

        transcript=transcript
    )


def ingest_youtube(
    celebrity_name: str,
    youtube_urls: list[str],
) -> list[YouTubeDocument]:

    youtube_documents = [
        create_youtube_document(
            celebrity_name,
            youtube_url,
        )
        for youtube_url in youtube_urls
    ]

    save_youtube_documents(
        celebrity_name,
        youtube_documents,
    )

    return youtube_documents
