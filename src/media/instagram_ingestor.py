# src/media/instagram_ingestor.py

from src.media.instagram_document import (
    InstagramDocument
)


def detect_instagram_type(
    url: str
) -> str:
    """
    Detect whether the Instagram URL
    is a profile, post, or reel.
    """

    url = url.lower()

    if "/reel/" in url:

        return "reel"

    if "/p/" in url:

        return "post"

    return "profile"


def clean_instagram_text(
    text: str
) -> str:
    """
    Clean title/snippet text.
    """

    if not text:

        return ""

    text = text.strip()

    text = text.replace(
        "\n",
        " "
    )

    text = " ".join(
        text.split()
    )

    return text


def extract_username(
    url: str
) -> str:
    """
    Extract Instagram username
    from profile URL.
    """

    try:

        parts = (

            url
            .split(
                "instagram.com/"
            )[-1]
            .split("/")
        )

        if len(parts) > 0:

            username = parts[0]

            if username not in {

                "",

                "p",

                "reel",

                "explore"
            }:

                return username

        return ""

    except Exception:

        return ""


def create_instagram_document(
    celebrity_name: str,
    result
) -> InstagramDocument:
    """
    Convert a SearchResult
    into an InstagramDocument.
    """

    title = clean_instagram_text(

        result.title
    )

    content = clean_instagram_text(

        result.snippet
    )

    content_type = (
        detect_instagram_type(
            result.url
        )
    )

    username = (
        extract_username(
            result.url
        )
    )

    if username:

        content = (

            f"Instagram username: "
            f"{username}\n\n"

            f"{content}"
        )

    return InstagramDocument(

        celebrity=celebrity_name,

        source_type="instagram",

        title=title,

        url=result.url,

        content=content,

        content_type=content_type
    )


def create_instagram_documents(
    celebrity_name: str,
    instagram_results: list
) -> list:
    """
    Create Instagram documents
    from search results.
    """

    documents = []

    for result in instagram_results:

        try:

            document = (
                create_instagram_document(

                    celebrity_name,

                    result
                )
            )

            documents.append(
                document
            )

        except Exception as e:

            print(

                f"Failed to create "
                f"Instagram document: "
                f"{e}"
            )

    return documents


def print_instagram_documents(
    documents: list
):
    """
    Debug helper.
    """

    for document in documents:

        print()

        print(
            "=" * 60
        )

        print(
            document.title
        )

        print(
            document.content_type
        )

        print(
            document.url
        )

        print(
            document.content[
                :200
            ]
        )