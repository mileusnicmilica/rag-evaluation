"""Run the unchanged Week 7 metrics with the optional embedding retriever."""

import argparse
import json
from pathlib import Path

from . import config
from .chunking import build_chunks
from .corpus import load_corpus
from .embedding_retrieval import EMBEDDING_REFUSAL_THRESHOLD, MODEL_NAME
from .eval_runner import eval_set_sha256, evaluate_item, format_table, load_eval_set, summarise
from .rag import build_grounded_answer


def run_eval() -> dict:
    from datetime import datetime, timezone

    chunks = build_chunks(load_corpus())
    chunks_by_id = {chunk.chunk_id: chunk for chunk in chunks}
    rows = [
        evaluate_item(
            item,
            build_grounded_answer(item["question"], chunks, retrieval_mode="embeddings"),
            chunks_by_id,
        )
        for item in load_eval_set()
    ]
    return {
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "eval_set_sha256": eval_set_sha256(),
        "config": {
            **config.snapshot(),
            "RETRIEVAL_MODE": "embeddings",
            "EMBEDDING_MODEL": MODEL_NAME,
            "EMBEDDING_REFUSAL_THRESHOLD": EMBEDDING_REFUSAL_THRESHOLD,
        },
        "summary": summarise(rows),
        "results": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Week 7 eval with local embeddings")
    parser.add_argument("--out", required=True, help="Path for the embedding run JSON")
    args = parser.parse_args()

    run = run_eval()
    print(format_table(run))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(run, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
