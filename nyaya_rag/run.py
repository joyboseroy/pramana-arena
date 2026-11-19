"""Command line entry point.

  python -m nyaya_rag.run --question "Does device_7 support carrier aggregation?" \
      --passages data/nyaya_rag_sample_passages.json --context release=Rel-17 \
      --regime navya_nyaya

Needs the `anthropic` package and ANTHROPIC_API_KEY (this path has not been run against the
live API in this repo). The passages file is a JSON list of
{"id", "text", "source", "rank", "pramana"} objects.
"""
from __future__ import annotations

import argparse
import json

from .extract import Passage
from .llm import anthropic_llm
from .pipeline import render, run


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--question", required=True)
    ap.add_argument("--passages", required=True)
    ap.add_argument("--context", nargs="*", default=[], help="key=value pairs, e.g. release=Rel-17")
    ap.add_argument("--regime", default="navya_nyaya",
                    choices=["nyaya", "navya_nyaya", "dignaga", "dharmakirti", "jain"])
    ap.add_argument("--model", default="claude-sonnet-5-5")
    args = ap.parse_args()

    with open(args.passages, encoding="utf-8") as fh:
        passages = [Passage(**p) for p in json.load(fh)]
    context = dict(kv.split("=", 1) for kv in args.context)
    result = run(args.question, passages, context, anthropic_llm(args.model), args.regime)
    print(render(result))
    if result.skipped:
        print(f"\nSkipped passages (extraction failed): {', '.join(result.skipped)}")


if __name__ == "__main__":
    main()
