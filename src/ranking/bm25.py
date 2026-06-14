from rank_bm25 import BM25Okapi

from src.models.search_result import SearchResult


def tokenize(text: str):

    return text.lower().split()


def build_document(
    result: SearchResult
):

    return f"""
        {result.title}
        {result.title}
        {result.snippet}
        {result.snippet}
        {result.url}
"""


def bm25_rank(
    query: str,
    results: list[SearchResult]
):

    corpus = [
        tokenize(
            build_document(r)
        )
        for r in results
    ]

    bm25 = BM25Okapi(corpus)

    scores = bm25.get_scores(
        tokenize(query)
    )

    ranked = list(
        zip(results, scores)
    )

    ranked.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return ranked