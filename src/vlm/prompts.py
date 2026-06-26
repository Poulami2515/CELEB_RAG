# src/vlm/prompts.py

"""
Prompt templates for Vision-Language Models.

All image captioning prompts should be defined here
instead of inside model-specific implementations.
"""


# =====================================================
# Generic Image Captioning
# =====================================================

DEFAULT_IMAGE_CAPTION_PROMPT = """
Generate a detailed factual description of this image.

Guidelines:

- Describe only what is visually observable.
- Do not infer emotions, intentions, relationships, or events
  that are not directly visible.
- Mention:
    - people
    - clothing
    - objects
    - background
    - activities
    - colors
    - text visible in the image
- If the image contains a celebrity, describe the appearance
  without assuming identity unless explicitly provided.
- Use one concise paragraph.
"""


# =====================================================
# Instagram Image Captioning
# =====================================================

INSTAGRAM_IMAGE_PROMPT = """
You are captioning an Instagram image for a Retrieval-Augmented
Generation (RAG) knowledge base.

Generate an objective description of everything visible.

Include:

- people
- clothing
- pose
- facial expression (only if clearly visible)
- objects
- location or setting
- vehicles
- animals
- food
- accessories
- background
- readable text
- logos
- colors

Do NOT:

- invent facts
- speculate
- infer emotions
- infer identities beyond the provided context

The caption should be factual, concise, and information-rich.
"""


# =====================================================
# Movie Poster Prompt
# =====================================================

MOVIE_POSTER_PROMPT = """
Describe this movie poster.

Include:

- title
- actors visible
- clothing
- setting
- objects
- colors
- typography
- visible text
- logos
- overall composition

Do not infer the movie plot.
"""


# =====================================================
# News Image Prompt
# =====================================================

NEWS_IMAGE_PROMPT = """
Describe this news image factually.

Mention:

- people
- objects
- vehicles
- buildings
- background
- readable signs
- weather
- actions that are directly observable

Avoid speculation.
"""


# =====================================================
# Twitter/X Prompt
# =====================================================

TWITTER_IMAGE_PROMPT = """
Generate an objective caption for this social media image.

Focus on:

- people
- objects
- activities
- background
- text
- logos
- visual context

Avoid opinions or assumptions.
"""


# =====================================================
# YouTube Thumbnail Prompt
# =====================================================

YOUTUBE_THUMBNAIL_PROMPT = """
Describe this YouTube thumbnail.

Mention:

- people
- facial expressions
- objects
- background
- visible text
- logos
- colors
- layout

Keep the description factual.
"""