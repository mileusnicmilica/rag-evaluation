"""Re-run the separate Week 7 embedding experiment using the existing local model."""

import json
from pathlib import Path

from src import embedding_retrieval


ROOT = Path(__file__).resolve().parent
MODEL_CACHE = ROOT.parent / "rag-week-7-weak-checkpoint" / "rag-week-7-week-checkpoint" / ".cache" / "fastembed"
if not MODEL_CACHE.is_dir():
    raise SystemExit(f"Local embedding model cache not found: {MODEL_CACHE}")
embedding_retrieval.MODEL_CACHE = MODEL_CACHE

from src.chunking import build_chunks  # noqa: E402
from src.corpus import load_corpus  # noqa: E402
from src.embedding_eval import run_eval  # noqa: E402
from src.eval_runner import format_table  # noqa: E402
from src.rag import build_grounded_answer  # noqa: E402


def main() -> None:
    run = run_eval()
    print(format_table(run))
    output = ROOT / "results" / "live-demo.json"
    output.write_text(json.dumps(run, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nWrote {output}")

    chunks = build_chunks(load_corpus())
    by_id = {chunk.chunk_id: chunk for chunk in chunks}
    questions = {
        "E05": "How long until I get a new notebook computer?",
        "E06": "How many days per week can I work remotely?",
        "E10": "What is the current company stock price?",
        "E11": "What is the parental leave policy?",
    }
    for question_id, question in questions.items():
        result = build_grounded_answer(question, chunks, retrieval_mode="embeddings")
        print(f"\n{question_id}: {question}\n{result.answer}")
        for chunk_id in result.citations:
            chunk = by_id[chunk_id]
            print(f"Citation: {chunk_id} (version {chunk.version}, {chunk.status})")


if __name__ == "__main__":
    main()
