from pathlib import Path
import base64
import mimetypes
import os

from dotenv import load_dotenv
from openai import OpenAI

from src.vlm.base import BaseVisionLanguageModel
from src.vlm.prompts import INSTAGRAM_IMAGE_PROMPT


load_dotenv()


class OpenRouterVisionLanguageModel(BaseVisionLanguageModel):
    """
    Vision-Language Model implementation using
    OpenRouter + Google Gemma 4 31B (free).
    """

    MODEL_NAME = "google/gemma-4-31b-it:free"

    def __init__(self):

        api_key = os.getenv(
            "OPENROUTER_API_KEY"
        )

        if not api_key:

            raise ValueError(
                "OPENROUTER_API_KEY not found."
            )

        self.client = OpenAI(

            api_key=api_key,

            base_url="https://openrouter.ai/api/v1"
        )

    # ---------------------------------------------

    def load_model(self):

        """
        API models do not require explicit loading.
        """

        return

    # ---------------------------------------------

    def unload_model(self):

        """
        API models do not occupy local GPU memory.
        """

        return

    # ---------------------------------------------

    @staticmethod
    def image_to_base64(
        image_path: Path
    ) -> str:

        with open(
            image_path,
            "rb"
        ) as file:

            return base64.b64encode(
                file.read()
            ).decode(
                "utf-8"
            )

    # ---------------------------------------------

    def caption_image(
        self,
        image_path: Path,
        prompt: str = INSTAGRAM_IMAGE_PROMPT
    ) -> str:

        if not image_path.exists():

            raise FileNotFoundError(
                image_path
            )

        mime_type = mimetypes.guess_type(
            image_path
        )[0]

        if mime_type is None:

            mime_type = "image/jpeg"

        image_base64 = self.image_to_base64(
            image_path
        )

        response = self.client.chat.completions.create(

            model=self.MODEL_NAME,

            messages=[

                {

                    "role": "user",

                    "content": [

                        {

                            "type": "text",

                            "text": prompt

                        },

                        {

                            "type": "image_url",

                            "image_url": {

                                "url":

                                f"data:{mime_type};base64,{image_base64}"

                            }

                        }

                    ]

                }

            ],

            temperature=0.2,

            max_tokens=300

        )

        content = (
            response
            .choices[0]
            .message
            .content
        )

        if content is None:
            raise ValueError(
                "OpenRouter returned empty caption"
            )

        return content.strip()

    # ---------------------------------------------

    def batch_caption(
        self,
        image_paths: list[Path]
    ) -> list[str]:

        captions = []

        for image in image_paths:

            try:

                caption = self.caption_image(
                    image
                )

            except Exception as e:

                print(

                    f"Caption failed for "

                    f"{image.name}: "

                    f"{e}"

                )

                caption = ""

            captions.append(
                caption
            )

        return captions