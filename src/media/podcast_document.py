from pydantic import BaseModel


class PodcastDocument(
    BaseModel
):

    celebrity: str

    source_type: str = "podcast"

    title: str

    url: str

    description: str = ""

    platform: str = ""

    duration: int = 0