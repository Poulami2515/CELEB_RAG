from pathlib import Path

from src.vlm.openrouter import (
    OpenRouterVisionLanguageModel
)

from src.vlm.utils import (

    image_exists,

    caption_exists,

    save_caption,

    update_metadata

)

from src.storage.document_store import (
    get_celebrity_directory
)


# ==========================================================
# Helper
# ==========================================================

def get_instagram_media_directory(
    celebrity_name: str
) -> Path:

    return (

        get_celebrity_directory(
            celebrity_name
        )

        /

        "instagram_media"

    )


# ==========================================================
# Caption Single Post
# ==========================================================

def caption_instagram_post(

    vlm: OpenRouterVisionLanguageModel,

    post_directory: Path

):

    if not image_exists(

        post_directory

    ):

        return

    if caption_exists(

        post_directory

    ):

        print(

            f"Skipping "

            f"{post_directory.name}"

        )

        return

    image_path = (

        post_directory

        /

        "image.jpg"

    )

    try:

        caption = (

            vlm.caption_image(
                image_path
            )

        )

        save_caption(

            post_directory,

            caption

        )

        update_metadata(

            post_directory,

            vlm_caption_generated=True

        )

        print(

            f"Captioned "

            f"{post_directory.name}"

        )

    except Exception as e:

        print(

            f"Failed "

            f"{post_directory.name}: "

            f"{e}"

        )


# ==========================================================
# Caption Celebrity
# ==========================================================

def caption_instagram_media(

    celebrity_name: str

):

    media_directory = (

        get_instagram_media_directory(

            celebrity_name

        )

    )

    if not media_directory.exists():

        print(

            "Instagram media "

            "not found."

        )

        return

    vlm = (

        OpenRouterVisionLanguageModel()

    )

    vlm.load_model()

    post_directories = sorted(

        [

            path

            for path

            in media_directory.iterdir()

            if path.is_dir()

        ]

    )

    print()

    print(

        f"Captioning "

        f"{len(post_directories)} "

        f"posts..."

    )

    print()

    for post_directory in post_directories:

        caption_instagram_post(

            vlm,

            post_directory

        )

    vlm.unload_model()

    print()

    print(

        "Captioning complete."

    )