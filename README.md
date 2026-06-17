# FOLDER STRUCTURE:

```
CELEB_RAG/
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
├── requirements.txt
│
├── searxng/
│   └── settings.yml
│
├── src/
│   ├── main.py
│   │
│   ├── extraction/
│   │   └── webpage_extractor.py
│   │
│   ├── ingestion/
│   │   ├── celebrity_ingestor.py
│   │   └── query_generator.py
│   │
│   ├── media/
│   │   ├── image_ingestor.py
│   │   ├── instagram_document.py      ← new
│   │   ├── instagram_ingestor.py      ← updated
│   │   ├── instagram_pipeline.py      ← new
│   │   ├── instagram_search.py        ← new
│   │   ├── podcast_document.py
│   │   ├── podcast_ingestor.py
│   │   ├── podcast_pipeline.py
│   │   ├── podcast_search.py
│   │   ├── twitter_ingestor.py
│   │   ├── whisper_provider.py
│   │   ├── youtube_ingestor.py
│   │   ├── youtube_pipeline.py
│   │   └── youtube_search.py
│   │
│   ├── models/
│   │   ├── extracted_document.py
│   │   ├── search_result.py
│   │   └── youtube_document.py
│   │
│   ├── ranking/
│   │   └── bm25.py
│   │
│   ├── search/
│   │   ├── aggregator.py
│   │   ├── duckduckgo.py
│   │   ├── searxng.py
│   │   ├── storage.py
│   │   └── utils.py
│   │
│   └── storage/
│       ├── document_store.py          ← updated
│       └── failure_store.py
│
├── storage/
│   ├── failed_youtube_urls.json
│   └── celebrities/
│       ├── deepika_padukone/
│       │   ├── documents.json
│       │   ├── metadata.json
│       │   └── youtube_documents.json
│       ├── rick_astley/
│       │   └── youtube_documents.json
│       └── shah_rukh_khan/
│           ├── documents.json
│           ├── metadata.json
│           ├── instagram_documents.json   ← new
│           ├── podcast_documents.json
│           └── youtube_documents.json
│
└── tests/
    ├── test_audio_download.py
    ├── test_instagram_ingestor.py     ← new
    ├── test_instagram_pipeline.py     ← new
    ├── test_instagram_search.py       ← new
    ├── test_podcast_pipeline.py
    ├── test_podcast_search.py
    ├── test_whisper.py
    ├── test_whisper_fallback.py
    ├── test_youtube.py
    ├── test_youtube_document.py
    ├── test_youtube_search.py
    └── test_youtube_stotage.py
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
