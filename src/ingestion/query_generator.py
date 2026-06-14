# src/ingestion/query_generator.py

INGESTION_TEMPLATES = [
    "{name}",

    "{name} wikipedia",
    "{name} imdb",
    "{name} bbc",
    "{name} britannica",
    "{name} indianexpress",
    "{name} indiatoday",
    "{name} filmfare",
    "{name} vogue",
    "{name} forbes",

    "{name} biography",
    "{name} career",
    "{name} awards",
    "{name} achievements",
    "{name} filmography",
    "{name} interviews",
    "{name} personal life",
    "{name} family",
    "{name} education",
    "{name} business ventures",
    "{name} philanthropy",
    "{name} controversies",
    "{name} latest news"
]



def generate_queries(
    celebrity_name: str
):

    queries = [
        template.format(
            name=celebrity_name
        )
        for template in INGESTION_TEMPLATES
    ]

    return list(
        dict.fromkeys(queries)
    )