# instagram_document.py

from pydantic import BaseModel


class InstagramDocument(
    BaseModel
):

    celebrity: str

    source_type: str = "instagram"

    title: str

    url: str

    content: str

    content_type: str