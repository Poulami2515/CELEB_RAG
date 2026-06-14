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
