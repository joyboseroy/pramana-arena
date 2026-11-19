# Nyaya-RAG: pramana-typed evidence and fallacy checking for retrieved answers

Working title: *Nyaya-RAG: An Epistemically Structured Architecture for Evidence-Grounded LLM Reasoning*.

Status: design plus a small runnable scaffold (`nyaya_rag/`). The scaffold checks structured claims. The extraction step from raw text to claims is not built.

## The idea

Conventional RAG treats every retrieved passage as equally authoritative and rarely says how the answer follows from it. Nyaya gives two things that map onto this problem: a typed account of where knowledge comes from, and a fixed list of ways an inference goes wrong.

Every answer must state: source, then evidence type, then inference, then the rule used, then the conclusion.

## Evidence types

| Pramana | In a RAG system |
|---|---|
| pratyaksa | direct observation: tool output, database value, executed query |
| sabda | testimony: a retrieved document, statute or specification |
| anumana | derived from other evidence by a stated rule |
| upamana | by analogy to a retrieved similar case |

Most RAG evidence is sabda, yet answers are usually written as if observed. Typing the evidence makes that visible and lets a higher-ranked source (a newer release, a statute over a commentary, a database over a document) override a lower one.

## The five-member argument

pratijna (claim), hetu (reason), udaharana (general rule with examples), upanaya (the reason holds here, with evidence), nigamana (conclusion). In code: `nyaya_rag/schema.py::Argument`.

## Fallacies as RAG failure modes

| Nyaya fallacy | RAG failure it detects | How the scaffold detects it |
|---|---|---|
| asiddha | cited evidence is missing or does not assert the reason | cited ids absent or claim not found |
| savyabhicara | an overgeneralised rule with a counterexample in the corpus | instances where the reason holds and the claim fails |
| satpratipaksa | two sources of equal rank conflict | same subject and predicate, different value, equal rank |
| badhita | a higher-ranked source overrides (newer release, operator override) | contradicting claim with higher rank |
| viruddha | the reason supports the opposite conclusion | via the engine's wheel logic on the instances |
| upadhi (Navya-Nyaya) | a hidden condition on the rule is not met (jurisdiction, release) | rule `conditions` versus query context |

## Swappable validity regimes (the experimental handle)

The checker calls the engines from `pramana/engines.py`. Switching the regime changes how strict the system is:

- nyaya: five characteristics and five fallacies
- navya_nyaya: adds the upadhi test
- dharmakirti: rejects unless the source states a connection by identity or causation
- dignaga: the nine-fold wheel
- jain: a single necessary-connection criterion

Run `python -m nyaya_rag.demo` to see all five regimes on six synthetic scenarios. Findings to measure properly: how precision and recall of "reject" trade off across regimes, and which failure mode each regime catches.

## Evaluation plan

Baselines: plain RAG; RAG with citations; chain-of-thought RAG; RAG with an NLI self-check.

Metrics: claim-level faithfulness; overclaim rate; conflict-detection rate; abstention calibration; token and latency cost.

Ablations: structure only with no checker; checker only with no typed evidence; each regime in turn.

Testbeds: a release-drift question set (newer versions override older, the badhita case), and an Indian-law question set (statute over commentary, jurisdiction as upadhi).

## Hypotheses and risks

- H1: typed evidence plus checking reduces unsupported inferential leaps.
- H2: it detects conflicting sources better than citation-only RAG.
- H3: the cost in tokens and latency stays acceptable.
- Risk: structure may only add verbosity. The structure-only ablation exists to test this.
- Risk: the checker is only as good as claim extraction. Measure extraction error separately and report it.
- Novelty: structured arguments, attributed QA and claim verification all exist. Check related work before claiming novelty. The proposed contribution is the pramana typing, the fallacy taxonomy as a failure-mode detector, and the swappable regimes.

## Pipeline (built)

`nyaya_rag/pipeline.py::run` does the following:

1. **Extract.** For each passage, `extract.py` prompts an LLM for claims, rules and instances, reusing a growing shared vocabulary of predicate names so records from different passages line up. Output is validated. A malformed response skips that passage and records its id instead of crashing.
2. **Argue.** A second prompt asks for a five-member argument that cites only extracted evidence ids, or an explicit abstain.
3. **Check.** `bridge.check` builds a pramana-arena `Case` and runs the chosen regime.
4. **Repair or stop.** On a fallacy, the label and reason go back to the model for one repair attempt (`max_repairs`). If it cannot do better it abstains. Accepted answers are rendered with evidence types by `render`.

The prompts are in `extract.py` (EXTRACT_PROMPT) and `pipeline.py` (ARGUE_PROMPT, REPAIR_PROMPT). `ScriptedLLM` runs the whole flow offline in the tests (`tests/test_pipeline.py`). `anthropic_llm` and `python -m nyaya_rag.run` are written but have not been run against a live model, so expect to tune the prompts on first real use.

Known limits of this version:
- Contradiction is detected only for the same subject and predicate with a different value. Paraphrased or numeric conflicts need a normalisation step.
- The model chooses the argument. The checker catches bad ones but does not search for good ones.
- Ranks are supplied with each passage. Deriving them (release dates, source hierarchy) is a separate task.

## Next steps

1. Run `python -m nyaya_rag.run` on the sample passages with a real model and read the extraction outputs.
2. Build a labelled question set (answerable, unsupported, conflicting, superseded, conditional) from one testbed.
3. Compare against plain RAG on faithfulness and overclaim rate, with the ablations above.
