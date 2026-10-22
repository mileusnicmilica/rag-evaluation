"""Optional local semantic retrieval for the advanced experiment."""

from functools import lru_cache
from math import sqrt
from pathlib import Path

from . import config
from .chunking import Chunk
from .retrieval import RetrievalResult, searchable_chunks


MODEL_NAME = "BAAI/bge-small-en-v1.5"
EMBEDDING_REFUSAL_THRESHOLD = 0.75
MODEL_CACHE = Path(__file__).resolve().parents[1] / ".cache" / "fastembed"


@lru_cache(maxsize=1)
def _model():
    try:
        from fastembed import TextEmbedding
    except ImportError as error:
        raise RuntimeError(
            "Embedding mode needs the optional dependencies: "
            "pip install -r requirements-embeddings.txt"
        ) from error
    return TextEmbedding(model_name=MODEL_NAME, cache_dir=str(MODEL_CACHE))


@lru_cache(maxsize=4)
def _passage_vectors(texts: tuple[str, ...]):
    return tuple(_model().passage_embed(list(texts)))


def cosine_similarity(left, right) -> float:
    numerator = sum(float(a) * float(b) for a, b in zip(left, right))
    left_norm = sqrt(sum(float(value) ** 2 for value in left))
    right_norm = sqrt(sum(float(value) ** 2 for value in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def retrieve_top_k_embeddings(
    query: str, chunks: list[Chunk], k: int | None = None
) -> list[RetrievalResult]:
    """Rank chunks by cosine similarity between local query/passage embeddings."""
    k = config.TOP_K if k is None else k
    if k <= 0:
        raise ValueError("k must be > 0")

    candidates = searchable_chunks(chunks)
    if not candidates:
        return []

    passage_vectors = _passage_vectors(tuple(chunk.text for chunk in candidates))
    if len(passage_vectors) != len(candidates):
        raise RuntimeError("The embedding model returned an unexpected number of passage vectors")
    query_vector = next(iter(_model().query_embed([query])))
    scored = [
        RetrievalResult(chunk=chunk, score=cosine_similarity(query_vector, vector))
        for chunk, vector in zip(candidates, passage_vectors)
    ]
    scored.sort(key=lambda item: (-item.score, item.chunk.chunk_id))
    return scored[:k]
