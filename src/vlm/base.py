# src/vlm/base.py

from abc import ABC, abstractmethod
from pathlib import Path


class BaseVisionLanguageModel(ABC):
    """
    Abstract base class for all Vision-Language Models (VLMs).

    Every VLM implementation must inherit from this class.
    """

    @abstractmethod
    def load_model(self) -> None:
        """
        Load the Vision-Language Model into memory.
        """
        pass

    @abstractmethod
    def unload_model(self) -> None:
        """
        Free model resources from memory.
        """
        pass

    @abstractmethod
    def caption_image(
        self,
        image_path: Path
    ) -> str:
        """
        Generate a caption for an image.

        Parameters
        ----------
        image_path : Path

        Returns
        -------
        str
        """
        pass

    @abstractmethod
    def batch_caption(
        self,
        image_paths: list[Path]
    ) -> list[str]:
        """
        Caption multiple images.

        Parameters
        ----------
        image_paths : list[Path]

        Returns
        -------
        list[str]
        """
        pass