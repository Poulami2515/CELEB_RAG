# FOLDER STRUCTURE:

```
celeb_rag/
├── .env.example              # template for SEARXNG_URL
├── .gitignore
├── docker-compose.yml        # local SearXNG (Docker)
├── requirements.txt
│
├── searxng/
│   └── settings.yml          # SearXNG config (json format enabled)
│
├── src/
│   ├── main.py               # entry point
│   │
│   ├── models/
│   │   ├── search_result.py
│   │   └── extracted_document.py
│   │
│   ├── search/
│   │   ├── aggregator.py     # DuckDuckGo + SearXNG
│   │   ├── duckduckgo.py
│   │   ├── searxng.py
│   │   ├── storage.py        # saves search_results.json
│   │   └── utils.py
│   │
│   ├── ranking/
│   │   └── bm25.py
│   │
│   ├── ingestion/
│   │   ├── query_generator.py
│   │   └── celebrity_ingestor.py   # full pipeline
│   │
│   ├── extraction/
│   │   └── webpage_extractor.py
│   │
│   ├── storage/
│   │   └── document_store.py       # save/load documents + metadata
│   │
│   └── media/                      # stubs (empty for now)
│       ├── youtube_ingestor.py
│       ├── twitter_ingestor.py
│       ├── instagram_ingestor.py
│       ├── tiktok_ingestor.py
│       ├── image_ingestor.py
│       └── podcast_ingestor.py
│
├── .env                        # your local secrets/config
├── .venv/                      # Python virtual environment
├── pyrightconfig.json          # editor/type-checker config
├── .vscode/                    # editor settings
├── data/                       # raw search result dumps
├── storage/                    # ingested celebrity documents
│   └── celebrities/
│       └── <celebrity_name>/
│           ├── documents.json
│           └── metadata.json
└── *.pptx                      # progress decks (gitignored)
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
