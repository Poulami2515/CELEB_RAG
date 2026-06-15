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
│   │   ├── instagram_ingestor.py
│   │   ├── podcast_ingestor.py
│   │   ├── tiktok_ingestor.py
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
│       ├── document_store.py
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
│           └── metadata.json
│
└── tests/
    ├── test_audio_download.py
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
