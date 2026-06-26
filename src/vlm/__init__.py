"""
Vision-Language Model (VLM) package.

Provides reusable interfaces for image captioning
using different backend providers.
"""

from .base import BaseVisionLanguageModel
from .openrouter import OpenRouterVisionLanguageModel

__all__ = [

    "BaseVisionLanguageModel",

    "OpenRouterVisionLanguageModel",

]