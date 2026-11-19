# Divergence report
13 cases, 6 engines. A star marks a case where engines disagree.

## Stipulated mode (pure logic): 4 of 13 cases diverge
| Case | Dignaga | Dharmakirti | Nyaya | Navya-Nyaya | Jain | Carvaka (baseline) |
|---|---|---|---|---|---|---|
| smoke-fire | valid | valid | valid | valid | valid | invalid |
| produced-impermanent | valid | valid | valid | valid | valid | invalid |
| audible-eternal | invalid | invalid | invalid | invalid | invalid | invalid |
| knowable-impermanent | invalid | invalid | invalid | invalid | invalid | invalid |
| produced-eternal | invalid | invalid | invalid | invalid | invalid | invalid |
| knowable-nameable * | n/a | invalid | valid | valid | n/a | invalid |
| earth-smell * | n/a | invalid | valid | valid | n/a | invalid |
| krttika-rohini * | invalid | invalid | invalid | invalid | valid | invalid |
| tatputratva * | valid | invalid | valid | invalid | invalid | invalid |
| existence-momentary | n/a | valid | valid | valid | valid | invalid |
| hill-smoke-from-fire | invalid | invalid | invalid | invalid | invalid | invalid |
| no-pot | valid | valid | n/a | n/a | n/a | invalid |
| fire-cold | invalid | invalid | invalid | invalid | invalid | invalid |

## Native mode (logic plus each school's ontology): 5 of 13 cases diverge
| Case | Dignaga | Dharmakirti | Nyaya | Navya-Nyaya | Jain | Carvaka (baseline) |
|---|---|---|---|---|---|---|
| smoke-fire | valid | valid | valid | valid | valid | invalid |
| produced-impermanent | valid | valid | valid | valid | valid | invalid |
| audible-eternal | invalid | invalid | invalid | invalid | invalid | invalid |
| knowable-impermanent | invalid | invalid | invalid | invalid | invalid | invalid |
| produced-eternal | invalid | invalid | invalid | invalid | invalid | invalid |
| knowable-nameable * | n/a | invalid | valid | valid | n/a | invalid |
| earth-smell * | n/a | invalid | valid | valid | n/a | invalid |
| krttika-rohini * | invalid | invalid | invalid | invalid | valid | invalid |
| tatputratva * | valid | invalid | valid | invalid | invalid | invalid |
| existence-momentary * | n/a | valid | invalid | invalid | invalid | invalid |
| hill-smoke-from-fire | invalid | invalid | invalid | invalid | invalid | invalid |
| no-pot | valid | valid | n/a | n/a | n/a | invalid |
| fire-cold | invalid | invalid | invalid | invalid | invalid | invalid |

## Where ontology changes a verdict
- existence-momentary, Nyaya: valid (stipulated) to invalid (native)
- existence-momentary, Navya-Nyaya: valid (stipulated) to invalid (native)
- existence-momentary, Jain: valid (stipulated) to invalid (native)

## Pairwise agreement, stipulated mode (agree / comparable cases)
| | Dignaga | Dharmakirti | Nyaya | Navya-Nyaya | Jain | Carvaka (baseline) |
|---|---|---|---|---|---|---|
| Dignaga | 10/10 | 9/10 | 9/9 | 8/9 | 7/9 | 6/10 |
| Dharmakirti | 9/10 | 13/13 | 9/12 | 10/12 | 9/10 | 9/13 |
| Nyaya | 9/9 | 9/12 | 12/12 | 11/12 | 8/10 | 6/12 |
| Navya-Nyaya | 8/9 | 10/12 | 11/12 | 12/12 | 9/10 | 7/12 |
| Jain | 7/9 | 9/10 | 8/10 | 9/10 | 10/10 | 6/10 |
| Carvaka (baseline) | 6/10 | 9/13 | 6/12 | 7/12 | 6/10 | 13/13 |

## Divergent cases in detail (stipulated mode)
### knowable-nameable: The pot is nameable because knowable
*The pot is nameable, because it is knowable.* Confidence of the case annotation: **canonical-nyaya**.
- Dignaga: **n/a**, outside the wheel
- Dharmakirti: **invalid**, no pratibandha
- Nyaya: **valid**, valid (kevalanvayi)
- Navya-Nyaya: **valid**, valid (kevalanvayi)
- Jain: **n/a**, unannotated
- Carvaka (baseline): **invalid**, anumana not a pramana

Note: Nyaya's standard kevalanvayi example (nothing is unnameable). Jain annotation left empty: anekanta and avaktavya may block the premise. Needs a scholar's reading.

### earth-smell: Earth differs from the other elements because it has smell
*Earth differs from the other elements, because it has smell.* Confidence of the case annotation: **canonical-nyaya**.
- Dignaga: **n/a**, outside the wheel
- Dharmakirti: **invalid**, no pratibandha
- Nyaya: **valid**, valid (kevalavyatireki)
- Navya-Nyaya: **valid**, valid (kevalavyatireki)
- Jain: **n/a**, unannotated
- Carvaka (baseline): **invalid**, anumana not a pramana

Note: Nyaya's standard kevalavyatireki example, valid by negative concomitance alone.

### krttika-rohini: Rohini will rise because Krttika has risen
*Rohini will rise soon, because Krttika has risen.* Confidence of the case annotation: **disputed**.
- Dignaga: **invalid**, asiddha
- Dharmakirti: **invalid**, asiddha
- Nyaya: **invalid**, asiddha
- Navya-Nyaya: **invalid**, asiddha
- Jain: **valid**, anyathanupapanna
- Carvaka (baseline): **invalid**, anumana not a pramana

Note: Used in the Jain case that pakshadharmata is not required. Buddhist and Nyaya replies may redefine the subject; the engines show only the structural verdicts.

### tatputratva: He is dark because he is her son
*This child is dark, because he is her son.* Confidence of the case annotation: **needs-philological-check**.
- Dignaga: **valid**, hetu-cakra case 2: valid
- Dharmakirti: **invalid**, no pratibandha
- Nyaya: **valid**, valid (anvaya-vyatireki)
- Navya-Nyaya: **invalid**, sopadhika (vyapti fails)
- Jain: **invalid**, no anyathanupapatti
- Carvaka (baseline): **invalid**, anumana not a pramana

Note: Classically cited as a case where the three characteristics hold yet the inference fails, with a hidden factor (the mother's diet) as the upadhi. Check the exact formulation in the sources before citing.
