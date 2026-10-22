from src import embedding_retrieval
from src.chunking import Chunk


def test_embedding_retrieval_uses_vector_similarity_and_keeps_citations(monkeypatch) -> None:
    class FakeModel:
        def passage_embed(self, texts):
            assert texts == ["laptop replacement", "annual leave"]
            return iter(([1.0, 0.0], [0.0, 1.0]))

        def query_embed(self, queries):
            assert queries == ["notebook computer"]
            return iter(([0.9, 0.1],))

    chunks = [
        Chunk("equipment-0", "equipment", "Equipment", "2026", "current", "laptop replacement"),
        Chunk("leave-0", "leave", "Leave", "2026", "current", "annual leave"),
    ]
    monkeypatch.setattr(embedding_retrieval, "_model", lambda: FakeModel())
    embedding_retrieval._passage_vectors.cache_clear()

    results = embedding_retrieval.retrieve_top_k_embeddings("notebook computer", chunks, k=2)

    assert [result.chunk.chunk_id for result in results] == ["equipment-0", "leave-0"]
    assert results[0].score > results[1].score
