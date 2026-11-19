"""LLM adapters. The pipeline only needs a function from prompt text to response text.

ScriptedLLM is for tests and offline development.
anthropic_llm is a thin adapter that has NOT been run against the live API in this repo;
it needs the `anthropic` package and ANTHROPIC_API_KEY. Swap in any other provider by
passing any callable with the same signature.
"""
from __future__ import annotations

from typing import Callable, List, Tuple

LLM = Callable[[str], str]


class ScriptedLLM:
    """Returns the first scripted response whose key appears in the prompt."""

    def __init__(self, script: List[Tuple[str, str]]):
        self.script = list(script)
        self.calls: List[str] = []

    def __call__(self, prompt: str) -> str:
        self.calls.append(prompt)
        for key, response in self.script:
            if key in prompt:
                return response
        raise KeyError(f"no scripted response for prompt starting: {prompt[:80]!r}")


def anthropic_llm(model: str = "claude-sonnet-5-5", max_tokens: int = 1500) -> LLM:
    import anthropic  # imported lazily so the rest of the repo has no dependencies

    client = anthropic.Anthropic()

    def call(prompt: str) -> str:
        msg = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")

    return call
