from pydantic import BaseModel

class ExtractedDocument(BaseModel):
    celebrity: str
    title: str
    url: str
    source: str
    snippet: str
    page_text: str