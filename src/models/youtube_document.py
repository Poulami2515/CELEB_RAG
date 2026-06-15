from pydantic import BaseModel


class YouTubeDocument(BaseModel):

    celebrity: str

    source_type: str = "youtube"

    video_id: str

    title: str

    url: str

    transcript: str