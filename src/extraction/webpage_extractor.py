import importlib.util
import pkgutil
import re
from typing import Any
from urllib.parse import urlparse

import requests
import trafilatura
from bs4 import BeautifulSoup

if not hasattr(pkgutil, "find_loader"):
    def find_loader(name: str):
        spec = importlib.util.find_spec(name)
        return spec.loader if spec else None

    pkgutil.find_loader = find_loader

from imdb import Cinemagoer
from readability import Document

from src.models.extracted_document import (
    ExtractedDocument
)


MIN_EXTRACTED_TEXT_LENGTH = 500
IMDB_PERSON_PATTERN = re.compile(r"/name/(nm\d+)/")


def _is_good_text(text: str) -> bool:
    return len(text.strip()) > MIN_EXTRACTED_TEXT_LENGTH


def _extract_with_trafilatura(html: str) -> str:
    text = trafilatura.extract(html)
    return text or ""


def _extract_with_readability(html: str) -> str:
    document = Document(html)
    summary_html = document.summary()
    soup = BeautifulSoup(summary_html, "html.parser")
    return soup.get_text(" ", strip=True)


def _extract_with_beautifulsoup(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    paragraphs = [
        paragraph.get_text(" ", strip=True)
        for paragraph in soup.find_all("p")
    ]

    return "\n".join(
        paragraph
        for paragraph in paragraphs
        if paragraph
    )


def _is_imdb_url(url: str) -> bool:
    domain = urlparse(url).netloc.lower()
    return domain == "imdb.com" or domain.endswith(".imdb.com")


def _format_imdb_value(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, list):
        return "\n".join(str(item) for item in value if item)

    return str(value)


def _format_imdb_credits(
    title: str,
    credits: list[Any],
    limit: int = 30,
) -> str:
    if not credits:
        return ""

    credit_names = [
        str(credit)
        for credit in credits[:limit]
    ]

    return f"{title}: " + ", ".join(credit_names)


def _extract_with_cinemagoer(url: str) -> str:
    match = IMDB_PERSON_PATTERN.search(url)
    if not match:
        return ""

    person_id = match.group(1).removeprefix("nm")
    imdb = Cinemagoer()
    person = imdb.get_person(person_id)

    try:
        imdb.update(person)
    except Exception:
        pass

    sections = [
        f"Name: {_format_imdb_value(person.get('name'))}",
        f"Birth date: {_format_imdb_value(person.get('birth date'))}",
        f"Birth notes: {_format_imdb_value(person.get('birth notes'))}",
    ]

    biography = (
        person.get("mini biography")
        or person.get("biography")
    )
    biography_text = _format_imdb_value(biography)
    if biography_text:
        sections.append(f"Biography:\n{biography_text}")

    filmography = person.get("filmography")
    if isinstance(filmography, dict):
        for role in (
            "actress",
            "actor",
            "producer",
            "writer",
            "director",
            "self",
        ):
            credits_text = _format_imdb_credits(
                role.title(),
                filmography.get(role, []),
            )
            if credits_text:
                sections.append(credits_text)

    return "\n\n".join(
        section
        for section in sections
        if section and not section.endswith(": ")
    )


def _fetch_html(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        return downloaded

    response = requests.get(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
        },
        timeout=20,
    )
    response.raise_for_status()
    return response.text


def extract_url(
    url: str
) -> str:

    try:
        if _is_imdb_url(url):
            imdb_text = _extract_with_cinemagoer(url)
            if _is_good_text(imdb_text):
                return imdb_text

        html = _fetch_html(url)

        trafilatura_text = _extract_with_trafilatura(html)
        if _is_good_text(trafilatura_text):
            return trafilatura_text

        readability_text = _extract_with_readability(html)
        if _is_good_text(readability_text):
            return readability_text

        beautifulsoup_text = _extract_with_beautifulsoup(html)
        if _is_good_text(beautifulsoup_text):
            return beautifulsoup_text

        return (
            trafilatura_text
            or readability_text
            or beautifulsoup_text
            or ""
        )

    except Exception:

        return ""


def create_document(
    celebrity_name: str,
    search_result
) -> ExtractedDocument:

    page_text = extract_url(
        search_result.url
    )

    return ExtractedDocument(

        celebrity=celebrity_name,

        title=search_result.title,

        url=search_result.url,

        source=search_result.source,

        snippet=search_result.snippet,

        page_text=page_text
    )