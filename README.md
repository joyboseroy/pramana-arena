# pramana-arena

Executable models of how Indian schools judge an inference, run side by side on the same cases. The aim is to find exactly where Dignaga and Dharmakirti, classical Nyaya, Navya-Nyaya, the Jains and (as a baseline) the Carvakas disagree, and to separate disagreement about *logic* from disagreement about *what exists*.

Status: starter scaffold. 13 hand-annotated cases, 6 engines, no external dependencies (Python 3.9+).

## Run it

```
python3 -m pramana.compare       # writes results/report.md, verdicts_*.json, matrix_*.csv
python3 -m pramana.inventory     # pramana sets and debate rules compared
python3 -m unittest discover -s tests -t .
```

## Design

Each inference is a `Case` (pramana/model.py) holding only structural facts: is the reason in the subject, how often it occurs in similar and dissimilar instances, what kind of reason it is, whether it is tied to the probandum by identity or causation, whether the thesis is contradicted, whether a hidden conditioning factor (upadhi) exists, whether a necessary connection holds (the Jain criterion). Cases carry no school's verdict.

Each engine (pramana/engines.py) is a small, readable formalisation of one school's validity criteria:

| Engine | Criterion modelled |
|---|---|
| Dignaga | pakshadharmata plus the nine-fold hetu-cakra (valid cases 2 and 8) |
| Dharmakirti | reason must be a svabhava, karya or anupalabdhi reason, tied to the probandum by identity or causation |
| Nyaya | five characteristics and five hetvabhasa; accepts kevalanvayi and kevalavyatireki; treats absence as perception |
| Navya-Nyaya | Nyaya plus the upadhi test on vyapti |
| Jain | a single characteristic, anyathanupapannatva (no pakshadharmata required) |
| Carvaka | inference is not a pramana (baseline, excluded from divergence counts) |

Engines may abstain (`n/a`) when a case is outside their scope, for example a kevalanvayi inference lies outside Dignaga's wheel.

### Logic versus ontology

The same inference has different sapaksa and vipaksa facts depending on what a school thinks exists. "Whatever exists is momentary" has no counterexample for a Buddhist and plenty for a Naiyayika. So there are two modes:

- **stipulated**: all engines see the case as written. Disagreement here is pure logic.
- **native**: each engine sees the case through its own school's `ontology` overrides. Disagreement here is logic plus ontology.

Current result: 4 of 13 cases diverge in stipulated mode, 5 in native mode. `existence-momentary` is the case that flips with ontology. See results/report.md.

## What the first run shows

The same inference goes in, and each school's criteria give a verdict. "n/a" means the engine abstains because the case lies outside its framework. The Carvaka column is a baseline (it rejects all inference), so it is left out of the divergence count. Rows marked * are cases where the schools disagree.

**Stipulated mode (pure logic), 4 of 13 cases diverge**

| Inference (thesis, because reason) | Dignaga | Dharmakirti | Nyaya | Navya-Nyaya | Jain |
|---|---|---|---|---|---|
| The hill has fire, because it has smoke | valid | valid | valid | valid | valid |
| Sound is impermanent, because it is produced | valid | valid | valid | valid | valid |
| Sound is eternal, because it is audible | invalid | invalid | invalid | invalid | invalid |
| Sound is impermanent, because it is knowable | invalid | invalid | invalid | invalid | invalid |
| Sound is eternal, because it is produced | invalid | invalid | invalid | invalid | invalid |
| The pot is nameable, because it is knowable * | n/a | invalid | valid | valid | n/a |
| Earth differs from the other elements, because it has smell * | n/a | invalid | valid | valid | n/a |
| Rohini will rise soon, because Krttika has risen * | invalid | invalid | invalid | invalid | valid |
| This child is dark, because he is her son * | valid | invalid | valid | invalid | invalid |
| The pot is momentary, because it exists | n/a | valid | valid | valid | valid |
| The hill has smoke, because it has fire | invalid | invalid | invalid | invalid | invalid |
| There is no pot on this table, because a pot, if present, would be seen, and is not seen | valid | valid | n/a | n/a | n/a |
| Fire is not hot, because it is a substance | invalid | invalid | invalid | invalid | invalid |

**Reading the disagreements**

- **Tatputratva** (the "he is dark because he is her son" case): Dignaga's criteria pass it, Dharmakirti, Navya-Nyaya and the Jain engine reject it, classical Nyaya passes it. One case, three different reasons for rejection.
- **Krttika-rohini**: only the Jain engine accepts it, because it does not require the reason to be a property of the subject.
- **Knowable-nameable and earth-smell**: Nyaya accepts both (kevalanvayi and kevalavyatireki reasoning), Dharmakirti rejects them for lacking a connection by identity or causation, and Dignaga's wheel has no cell for them.
- **Agreement on the textbook cases**: all five engines agree on the smoke, produced-sound and fallacy cases, so the encodings are at least consistent where the traditions are known to agree.

**Native mode (logic plus each school's own ontology), 5 of 13 diverge**

The only verdict that changes is "the pot is momentary, because it exists". Under stipulated facts every engine accepts it. Under each school's own ontology, Dharmakirti still accepts it (for a Buddhist, whatever exists is momentary, so no counterexample exists), while Nyaya, Navya-Nyaya and the Jain engine reject it (for them, enduring things exist, so the reason also occurs where the probandum does not). The inference rule is the same, and the verdict changes because the schools disagree about what exists. That is the distinction the logic-versus-ontology switch is built to expose.

Pairwise agreement on cases both engines can judge (stipulated mode): Dignaga and Nyaya 9 of 9, Nyaya and Navya-Nyaya 11 of 12, Dharmakirti and Nyaya 9 of 12, Dharmakirti and Jain 9 of 10, Nyaya and Jain 8 of 10. The full matrix is in results/report.md.

These are outputs of a first, small encoding, not findings. Each verdict is only as good as the rule behind it, and the citation ledger below shows which rules are checked against texts.

## Caveats

- Every rule is a hypothesis to check against primary texts and the specialist literature. Where I knew a point to be disputed, the case or engine says so.
- Case annotations have a `confidence` field. Anything marked `disputed` or `needs-philological-check` should not be cited until a scholar has looked at it.
- The nine-fold wheel numbering and the Nyaya treatment of viruddha (pervasion of the absence of the probandum, which differs slightly from Dignaga's cases 4 and 6) are modelling choices to verify.
- Jain, Mimamsa, Vedanta and Vaisesika are thin. The Jain annotations are the most hand-made.

## Textual basis and citation status

Not every rule is equally grounded, and the repo says so. docs/CITATIONS.md is a ledger that marks each modelling rule as verified, secondary or unverified, with the source. At present only a few Dharmakirti rules are checked against a text (the definition of a pramana through reliable action, and inference resting on invariable concomitance, both in the Pramanasiddhi chapter as translated by Nagatomi, 1957). The identity versus causation split, the three kinds of reason and the Nyaya, Navya-Nyaya and Jain rules still need passage pointers. None of the 13 cases has one yet.

Citing the Pramanavarttika: chapter numbering differs between sources (Nagatomi's "Book I" is the Pramanasiddhi chapter, which most current sources number 2). Details are in docs/CITATIONS.md.

## Related work

- Aditya Kumar Jha, "A Mathematical Model of Dignaga's Hetu-cakra", Journal of the Indian Council of Philosophical Research (2020): https://core.ac.uk/download/334592979.pdf
- Panday and Ghosh, "Cubical Type Theoretic Navya-Nyaya" (arXiv:2605.12548): a type-theoretic formalisation of Navya-Nyaya's technical language.
- Arjuna S. R. and Amba Kulkarni, Nyayacitradipika: a tool that parses Navya-Nyaya expressions into conceptual graphs (University of Hyderabad).
- Sathish, "Pramana: Fine-Tuning Large Language Models for Epistemic Reasoning through Navya-Nyaya" (arXiv:2604.04937), with a repository also called pramana. It fine-tunes models on a Nyaya method, while this repo uses a rule-based checker over retrieved evidence. Different approach, overlapping vocabulary, so expect confusion in names.
- Hayes and Gillon, "Introduction to Dharmakirti's theory of inference as presented in Pramanavarttika svopajnavrtti 1-10", Journal of Indian Philosophy 19 (1991). This is the main secondary source to check the Dharmakirti engine against.

What this repo adds: one shared case set run through several schools' criteria, with a switch that separates disagreement about logic from disagreement about what exists, and the use of those criteria as a swappable checker for retrieved answers. 

## Contributing

The most useful contribution is a case with a passage pointer: add an entry to data/cases.json with the structural facts, the source and the school's own verdict, and mark your confidence. Disagreements with an encoding are welcome as issues with a citation.

## Licence

MIT

## Roadmap

1. Grow the case set to about 100, each with a pointer to a passage (SOURCES.md lists texts).
2. Formal concept analysis over definitions of pratyaksa and vyapti across about a dozen thinkers.
3. Rule-swap debate arena: LLM agents debate, a referee scores the same transcript under the 22 nigrahasthana and under Dharmakirti's two grounds (data/debate_rules.json).
4. Objection-reply graph along the real chain Dignaga, Uddyotakara, Dharmakirti, Vacaspati, Santaraksita and Kamalasila, Udayana, Gangesa, loadable into Darshana Graph.
5. PramanaBench: do LLMs keep the schools' criteria apart?
6. Add Mimamsa (arthapatti, anupalabdhi as pramanas), Vaisesika (Prasastapada's formulation) and Advaita engines.

## Nyaya-RAG (second module)

`nyaya_rag/` uses the same engines as a checker for retrieved answers: evidence is typed by pramana, answers are five-member arguments, and fallacies (asiddha, savyabhicara, satpratipaksa, badhita, upadhi) become RAG failure modes. The validity regime is swappable, so strictness can be measured. The pipeline runs passages through LLM claim extraction, drafts a five-member argument, checks it, and repairs or abstains. It is tested offline with a scripted model; the live-model adapter is written but has not been run.

```
python3 -m nyaya_rag.demo        # six synthetic scenarios under five regimes
python3 -m nyaya_rag.run --question "Does device_7 support carrier aggregation?" \
    --passages data/nyaya_rag_sample_passages.json --context release=Rel-17   # needs anthropic and an API key
```

Design, evaluation plan and risks: docs/NYAYA_RAG.md.

## Layout

```
pramana/        model, engines, comparison runner, inventory
nyaya_rag/      typed evidence, extraction prompts, pipeline, bridge to the engines, CLI, demo
data/           cases.json, pramana_inventory.json, debate_rules.json
docs/           IDEAS.md (32 ideas, ranking, chosen focus), NYAYA_RAG.md,
                original_22_ideas.md (the earlier list, unchanged)
tests/          unit tests on canonical cases and on the Nyaya-RAG scenarios
results/        generated reports
SOURCES.md      where to download texts, with caveats
```
