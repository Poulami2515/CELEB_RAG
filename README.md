# FOLDER STRUCTURE:

```
CELEB_RAG/
├── .env                          # API keys (OpenRouter, etc.) — gitignored
├── .env.example
├── .gitignore
├── docker-compose.yml            # SearXNG search service (optional)
├── README.md
├── requirements.txt
│
├── searxng/
│   └── settings.yml              # SearXNG config (localhost:8080)
│
├── src/
│   ├── main.py                   # Orchestrates full ingestion pipeline
│   │
│   ├── extraction/
│   │   └── webpage_extractor.py  # Scrape & extract text from web pages
│   │
│   ├── ingestion/
│   │   ├── celebrity_ingestor.py   # Web ingestion entry point
│   │   └── query_generator.py        # Search query generation
│   │
│   ├── search/
│   │   ├── aggregator.py         # Combines SearXNG + DuckDuckGo
│   │   ├── duckduckgo.py
│   │   ├── searxng.py
│   │   ├── storage.py
│   │   └── utils.py
│   │
│   ├── ranking/
│   │   └── bm25.py
│   │
│   ├── models/
│   │   ├── extracted_document.py
│   │   ├── search_result.py
│   │   └── youtube_document.py
│   │
│   ├── storage/
│   │   ├── document_store.py     # Save/load all document types
│   │   └── failure_store.py      # Failed YouTube URL tracking
│   │
│   ├── media/                    # Media ingestion pipelines
│   │   ├── youtube_search.py
│   │   ├── youtube_ingestor.py
│   │   ├── youtube_pipeline.py   # YouTube: search → transcript → save
│   │   │
│   │   ├── podcast_search.py
│   │   ├── podcast_ingestor.py
│   │   ├── podcast_document.py
│   │   ├── podcast_pipeline.py   # Podcast: search → transcript → save
│   │   │
│   │   ├── instagram_search.py
│   │   ├── instagram_ingestor.py
│   │   ├── instagram_document.py
│   │   ├── instagram_pipeline.py # Instagram URLs + metadata
│   │   │
│   │   ├── instagram_media_ingestor.py   # Download posts/reels (instaloader)
│   │   ├── instagram_media_document.py
│   │   ├── instagram_media_pipeline.py     # Download → caption → transcribe
│   │   ├── instagram_captioner.py          # VLM image captions
│   │   ├── reel_transcriber.py             # Whisper reel transcription
│   │   │
│   │   ├── whisper_provider.py   # faster-whisper (GPU/CPU fallback)
│   │   ├── image_ingestor.py
│   │   └── twitter_ingestor.py
│   │
│   └── vlm/                      # Vision-Language Model (OpenRouter)
│       ├── __init__.py
│       ├── base.py
│       ├── openrouter.py
│       ├── prompts.py
│       └── utils.py
│
├── storage/                      # Generated data — gitignored
│   ├── failed_youtube_urls.json
│   └── celebrities/
│       └── <celebrity_slug>/     # e.g. shah_rukh_khan, katrina_kaif
│           ├── documents.json              # Web articles
│           ├── metadata.json               # Web ingestion metadata
│           ├── youtube_documents.json      # YouTube transcripts
│           ├── podcast_documents.json      # Podcast transcripts
│           ├── instagram_documents.json    # Instagram URL metadata
│           └── instagram_media/            # Downloaded media (when reachable)
│               └── <shortcode>/            # e.g. C4QXrpnvAEN
│                   ├── metadata.json
│                   ├── image.jpg             # or reel.mp4
│                   ├── caption.txt           # VLM-generated
│                   └── transcript.txt      # Whisper-generated (reels)
│
└── tests/
    ├── test_youtube.py
    ├── test_youtube_search.py
    ├── test_youtube_document.py
    ├── test_youtube_stotage.py
    ├── test_whisper.py
    ├── test_whisper_fallback.py
    ├── test_audio_download.py
    ├── test_podcast_search.py
    ├── test_podcast_pipeline.py
    ├── test_instagram_search.py
    ├── test_instagram_ingestor.py
    ├── test_instagram_pipeline.py
    ├── test_instagram_media_ingestor.py
    ├── test_instagram_captioner.py
    └── test_reel_transcriber.py
```


main.py

```
1. Web          → documents.json
2. YouTube      → youtube_documents.json
3. Podcast      → podcast_documents.json
4. Instagram    → instagram_documents.json
5. IG Media     → instagram_media/<shortcode>/  (blocked if Instagram unavailable)
```




Clone locally :

```
git clone https://github.com/Poulami2515/CELEB_RAG.git
cd CELEB_RAG
```

Create and activate a virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

Install packages:

```
pip install -r requirements.txt
```

Create your local .env from the example:
```
cp .env.example .env
```

Start SearXNG:
```
docker compose up -d
```

Then run the app:
```
python -m src.main
```

To update later after you make changes on GitHub:
```
cd CELEB_RAG
git pull
source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d
python -m src.main
```

# UPDATE RITUAL :

```
cd C:\Users\poulami.paul\PyCharmMiscProject\CELEB_RAG

git status

git add src/media/instagram_document.py src/media/instagram_pipeline.py src/media/instagram_search.py src/media/instagram_ingestor.py src/storage/document_store.py tests/test_instagram_ingestor.py tests/test_instagram_pipeline.py tests/test_instagram_search.py

git add src/media/tiktok_ingestor.py

git commit -m "Add Instagram ingestion pipeline and update media storage helpers."

git pull --rebase origin main

git push origin main
```
