# src/ingestion/celebrity_ingestor.py

from urllib.parse import urlparse

from src.ingestion.query_generator import generate_queries

from src.search.aggregator import search_all
from src.search.utils import deduplicate_results

from src.ranking.bm25 import bm25_rank

from src.extraction.webpage_extractor import create_document

from src.storage.document_store import save_documents, save_metadata


TOP_K_URLS = 40
ENABLE_TRUSTED_DOMAIN_FILTER = True

# Add trusted domains here later, then set ENABLE_TRUSTED_DOMAIN_FILTER = True.
TRUSTED_DOMAINS = [
    "wikipedia.org",
    "imdb.com",
    "bbc.com",
    "bbc.co.uk",
    "britannica.com",
    "indianexpress.com",
    "indiatoday.in",
    "news18.com",
    "filmfare.com",
    "vogue.in",
    "forbes.com",
    "hollywoodreporter.com",
    "bollywoodhungama.com",
    "filmibeat.com",
    "variety.com",
    "theguardian.com",
    "thehindu.com",
    "thetimesofindia.com",
    "theeconomic.com",
    "thehindustan.com",
]



def trusted_url(url: str) -> bool:
    domain = urlparse(url).netloc.lower()

    return any(
        trusted_domain in domain
        for trusted_domain in TRUSTED_DOMAINS
    )


def ingest_celebrity(
    celebrity_name: str
):
    """
    Full ingestion pipeline.

    1. Generate ingestion queries
    2. Search each query
    3. Aggregate results
    4. Deduplicate URLs
    5. BM25 rerank results
    6. Select top URLs
    7. Extract webpage content
    8. Save documents
    """

    print(f"\nStarting ingestion for {celebrity_name}")

    # --------------------------------------------------
    # Generate Queries
    # --------------------------------------------------

    queries = generate_queries(
        celebrity_name
    )

    print(
        f"Generated {len(queries)} queries"
    )

    # --------------------------------------------------
    # Search Queries
    # --------------------------------------------------

    all_results = []

    for query in queries:

        print(
            f"Searching: {query}"
        )

        try:

            results, stats = search_all(
                query
            )

            all_results.extend(
                results
            )

        except Exception as e:

            print(
                f"Search failed for "
                f"'{query}' -> {e}"
            )

    print(
        f"Collected {len(all_results)} URLs"
    )

    # --------------------------------------------------
    # Deduplicate
    # --------------------------------------------------

    unique_results = (
        deduplicate_results(
            all_results
        )
    )

    print(
        f"Unique URLs: "
        f"{len(unique_results)}"
    )

    # --------------------------------------------------
    # BM25 Rerank
    # --------------------------------------------------

    ranking_query = (
        f"{celebrity_name} biography career awards "
        f"filmography interviews latest news"
    )

    ranked_results = bm25_rank(
        ranking_query,
        unique_results
    )

    reranked_results = [
        result
        for result, score in ranked_results
    ]

    print(
        f"BM25 reranked URLs: "
        f"{len(reranked_results)}"
    )

    # --------------------------------------------------
    # Optional Trusted Domain Filter
    # --------------------------------------------------

    candidate_results = reranked_results

    if ENABLE_TRUSTED_DOMAIN_FILTER:
        candidate_results = [
            result
            for result in reranked_results
            if trusted_url(result.url)
        ]

        print(
            f"Trusted URLs: "
            f"{len(candidate_results)}"
        )

    # --------------------------------------------------
    # Select Top URLs
    # --------------------------------------------------

    selected_results = (
        candidate_results[:TOP_K_URLS]
    )

    print(
        f"Selected "
        f"{len(selected_results)} URLs"
    )

    # --------------------------------------------------
    # Extract Documents
    # --------------------------------------------------

    documents = []

    for result in selected_results:

        print(
            f"Extracting: "
            f"{result.url}"
        )

        try:

            document = create_document(
                celebrity_name,
                result
            )

            # Skip empty extractions

            if (
                document.page_text
                and len(document.page_text) > 500
            ):

                documents.append(
                    document
                )

        except Exception as e:

            print(
                f"Extraction failed "
                f"for {result.url}"
            )

    print(
        f"Successfully extracted "
        f"{len(documents)} documents"
    )

    # --------------------------------------------------
    # Save Documents
    # --------------------------------------------------

    save_documents(
        celebrity_name,
        documents
    )
    save_metadata(
        celebrity_name,
        len(documents),
        [doc.url for doc in documents]
    )

    print(
        f"Saved documents for "
        f"{celebrity_name}"
    )

    return documents