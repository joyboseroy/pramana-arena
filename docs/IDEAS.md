# Computational Buddhism and Indian philosophy: idea pool and ranking

The first 22 ideas come from `original_22_ideas.md` (saved from the earlier discussion, unchanged). Ideas 23 to 32 were added later. The ranking and the chosen focus follow.

## The 22 original ideas (titles)

1. Computational Madhyamaka (prasanga argument graphs)
2. DharmaBench-India / DharmaReason (philosophical reasoning benchmark)
3. Buddhist Concept Evolution Graph (temporal)
4. Computational Abhidharma
5. Buddhist Computational Psychology
6. Computational model of pratityasamutpada (simulator)
7. Buddhist argument mining
8. Buddhist intellectual genealogy
9. Buddhist textual phylogenetics
10. Buddhist translation alignment engine
11. "Same word, different philosophy" (word-sense disambiguation for doctrine)
12. Computational Buddhist hermeneutics (provenance of interpretation)
13. Buddhist hallucination benchmark (textual reliability)
14. Computational sectarian cartography
15. Buddhist concept drift
16. Computational comparison of Indian schools (Darshana Graph 2.0)
17. Jain anekantavada as computational logic
18. Nyaya as an AI reasoning architecture (Nyaya-RAG)
19. Buddhist epistemology benchmark
20. Computational meditation model
21. Buddhist practice knowledge graph
22. Dharma OS

## Ten added ideas

23. **Alaya-vijnana as sparse distributed memory.** Seeds and perfuming as write, consolidate and decay operations.
24. **Vinaya as executable law.** The rules as a defeasible rule base with offence classes and exceptions.
25. **Apoha as contrastive learning.** Concept by exclusion, compared with prototype and contrastive embeddings.
26. **Bardo as a state machine.** Tibetan intermediate-state sequence and the Abhidhamma death process as simulators.
27. **Catuskoti in four-valued logic.** Test whether LLMs keep "both" and "neither" apart.
28. **Hetu-cakra and trairupya verifier.** Executable checker for inferences. Built, see `pramana/`.
29. **Debate simulator with defeat conditions.** Multi-agent vada with a referee applying classical grounds of defeat.
30. **Recovering lost sutras from quotations.** Quotation graph over compendia such as the Siksasamuccaya.
31. **Transmission simulation.** Agent-based model of how texts and ideas moved along trade and monastic routes.
32. **Buddhist ethics alignment benchmark.** Dilemmas built on skilful means, precepts and bodhisattva vows, with a Right Speech rubric.

## Ranking by wow factor, effort and impact

| Rank | Idea | Effort | Why |
|---|---|---|---|
| 1 | 13 Textual reliability benchmark (merged with 2) | low | questions can be generated from Darshana Graph and checked against open corpora; benchmarks get cited |
| 2 | 25 Apoha as contrastive learning | low to medium | very original, small experiment |
| 3 | 23 Alaya-vijnana as SDM | low | reuses existing SDM code |
| 4 | 27 Catuskoti and prasanga stress test (with 1) | very low | about a week; pairs with the reductio benchmark |
| 5 | 6 Dependent origination simulator | low | most shareable visually |
| 6 | 18 Nyaya-RAG | low to medium | strongest appeal to engineers; scaffold in repo |
| 7 | 24 Vinaya as executable law | medium | open territory, reuses legal-AI pipeline |

Second tier: 11, 15 (need a clean dated corpus), 29, 30. Park for later: 9, 14, 12, 22, 21, because they depend on corpora that earlier items would build.

## Chosen focus

The Buddhist and Nyaya (plus Jain and other Indic) theories of inference, compared computationally. Two parts, both in this repo:

- `pramana/`: executable engines for Dignaga, Dharmakirti, Nyaya, Navya-Nyaya, Jain and a Carvaka baseline, run on a shared case set (ideas 28 and 17).
- `nyaya_rag/`: the same engines used as the checker for retrieved answers (idea 18).

Planned workstreams after the scaffold:

1. Grow the case set to about 100 with passage pointers.
2. Formal concept analysis over definitions of pratyaksa and vyapti across about a dozen thinkers.
3. Rule-swap debate arena: the same transcript scored under the 22 nigrahasthana and under Dharmakirti's two grounds.
4. Objection-reply graph along the Dignaga, Uddyotakara, Dharmakirti, Vacaspati, Udayana, Gangesa chain.
5. PramanaBench: do LLMs keep the schools' criteria apart?
