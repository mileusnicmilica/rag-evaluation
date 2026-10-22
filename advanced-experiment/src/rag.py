from dataclasses import dataclass

from . import config
from .chunking import Chunk, build_chunks
from .corpus import load_corpus
from .retrieval import RetrievalResult, retrieve_top_k


REFUSAL_MESSAGE = "I do not have enough grounded evidence in the provided corpus to answer that question."


@dataclass(frozen=True)
class RagAnswer:
    answer: str
    citations: list[str]
    refused: bool
    retrieved: list[RetrievalResult]


def select_citations(results: list[RetrievalResult]) -> list[RetrievalResult]:
    if config.CITATION_MIN_SCORE is not None:
        raise NotImplementedError("CITATION_MIN_SCORE is not implemented yet.")
    return results


def build_grounded_answer(
    question: str, chunks: list[Chunk], retrieval_mode: str = "lexical"
) -> RagAnswer:
    if retrieval_mode == "lexical":
        results = retrieve_top_k(question, chunks)
        refusal_threshold = config.REFUSAL_THRESHOLD
    elif retrieval_mode == "embeddings":
        from .embedding_retrieval import EMBEDDING_REFUSAL_THRESHOLD, retrieve_top_k_embeddings

        results = retrieve_top_k_embeddings(question, chunks)
        refusal_threshold = EMBEDDING_REFUSAL_THRESHOLD
    else:
        raise ValueError(f"Unknown retrieval mode: {retrieval_mode}")

    if not results or results[0].score < refusal_threshold:
        return RagAnswer(answer=REFUSAL_MESSAGE, citations=[], refused=True, retrieved=results)

    cited = select_citations(results)
    supporting_points = [f"[{item.chunk.chunk_id}] {item.chunk.text}" for item in cited]
    answer = "Grounded response based on retrieved context:\n" + "\n".join(supporting_points)
    return RagAnswer(
        answer=answer,
        citations=[item.chunk.chunk_id for item in cited],
        refused=False,
        retrieved=results,
    )


def answer_question(question: str) -> RagAnswer:
    return build_grounded_answer(question, build_chunks(load_corpus()))
