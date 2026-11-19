# Textual basis and citation status

This file says, for each modelling rule, how well it is grounded in a text. Status values:

- **verified**: checked against a passage in a source I could read (named below).
- **secondary**: stated in a secondary source I saw, not yet traced to the primary verse.
- **unverified**: standard in the literature as I understand it, but not checked here. Do not cite until checked.

## How to cite the Pramanavarttika (read this first)

The chapter order differs between sources, which makes bare "PV I" or "Book I" ambiguous.

| Chapter | Name | EAST / Gnoli convention | Nagatomi 1957 ("Book") |
|---|---|---|---|
| 1 | Svarthanumana (inference for oneself) | PV 1 (Gnoli 1960 prints it with the autocommentary, PVSV) | Book III |
| 2 | Pramanasiddhi | PV 2 | **Book I** |
| 3 | Pratyaksa | PV 3 | Book II |
| 4 | Pararthanumana | PV 4 | Book IV |

Nagatomi explains that the manuscripts give the order Svarthanumana, Pramanasiddhi, Pratyaksa, Pararthanumana, while the "natural" order that follows Dignaga's Pramanasamuccaya starts with Pramanasiddhi (Introduction, p. i). The OeAW EAST database uses the manuscript order (https://east.ikga.oeaw.ac.at/data/7/16/).

Rule for this repo: always write the chapter name, the numbering system and the edition, for example "PV 2 (Pramanasiddhi), Nagatomi verse 3 (Tibetan verse 1)". Never write "Book I" alone. Verse numbers also differ between editions (Sankrtyayana, Gnoli, Miyasaka), so give the edition.

## Ledger

| # | Rule or claim in the repo | Status | Basis | Used in |
|---|---|---|---|---|
| 1 | A pramana is a cognition free from contradiction (non-deceptive), where this consists in reliable success in purposive action (arthakriya) | verified | Nagatomi 1957, Pramanasiddhi verse 3 (Tibetan numbering 1), pp. 3 to 4, with the Introduction pp. v to vi. Check the Sanskrit in Sankrtyayana or Miyasaka. | docs/NYAYA_RAG.md (validity as tested by outcome) |
| 2 | Dharmakirti's test of validity is later and outcome-based, unlike the Mimamsa doctrine of self-validity | verified | Nagatomi's note to verse 3, p. 3 | docs/NYAYA_RAG.md |
| 3 | Inference rests on a reason that is invariably concomitant (avinabhava, vyapti) with the probandum | verified | Nagatomi, Pramanasiddhi verse 300 (Tibetan 287), pp. 257 to 258, which quotes the verse and Kamalasila's Tattvasangrahapanjika vol. I p. 12 | pramana/engines.py (dharmakirti, jain: necessary connection) |
| 4 | The Buddhist objects of knowledge are the particular (svalaksana, a point-instant) and the universal (samanyalaksana) | verified | Nagatomi, Introduction p. vii; note at pp. 105 to 106 | Buddhist ontology override in data/cases.json |
| 5 | Absence cannot be inferred from non-perception alone when the thing is invisible by nature, so the thing must be one that would be seen if present | verified as a commentator's point in a different context | Nagatomi, note to verse 128 (Tibetan 118:117), pp. 124 to 125, citing Prajnakaragupta's commentary p. 104 | `perceptible_if_present` field, dharmakirti engine, case `no-pot`. The primary pointer in PV 1 / PVSV is still missing |
| 6 | Dharmakirti has three kinds of reason: essential nature (svabhava), effect (karya), non-perception (anupalabdhi) | secondary | Wisdomlib page on Dharmakirti's reception: https://de.wisdomlib.org/buddhism/book/reverberations-of-dharmakirtis-philosophy/d/doc1143543.html | dharmakirti engine |
| 7 | The connection is by identity (tadatmya) for svabhava reasons and by causation (tadutpatti) for karya reasons | unverified | Standard in the literature as I understand it. Not found in the Nagatomi thesis, which does not cover PV 1. Trace it in PVSV 1 to 10 (Hayes and Gillon 1991) | dharmakirti engine, Case.relation |
| 8 | The inference of momentariness from existence (sattvanumana) is a Dharmakirtian inference, supported by a probative argument against the contrary | secondary | Same Wisdomlib page as row 6 | case `existence-momentary` |
| 9 | Dharmakirti denies that two valid reasons can conflict, unlike Dignaga's viruddhavyabhicarin | unverified | From general knowledge. Check the Hetubindu and PVSV before citing | dharmakirti engine (counter_reason) |
| 10 | Dignaga's wheel has nine cells (all, some, none for similar and dissimilar instances) and only cells 2 and 8 are sound | secondary | Wikipedia, Hetucakra: https://en.wikipedia.org/wiki/Hetucakra . The numbering in pramana/engines.py matches that page. Primary: Dignaga's Hetucakra and Pramanasamuccaya II | dignaga engine |
| 11 | Cells 4 and 6 are "contradictory", cell 5 "too specific" | unverified | My reading; the Wikipedia snippet I saw does not state it | WHEEL labels |
| 12 | Nyaya: five characteristics, five hetvabhasa, kevalanvayi and kevalavyatireki inferences accepted | unverified | Standard; check Nyayasutra 1.2 and Annambhatta's Tarkasamgraha, plus a Nyaya specialist | nyaya engine |
| 13 | Navya-Nyaya adds the upadhi test to vyapti | unverified | Standard; check Gangesa's Vyaptivada in the Tattvacintamani | navya_nyaya engine |
| 14 | Jain: the single criterion is anyathanupapannatva, and pakshadharmata is not required | unverified | Standard; check Pariksamukha and Pramanamimamsa on SARIT | jain engine, case `krttika-rohini` |
| 15 | Nyaya's 22 nigrahasthana and Dharmakirti's two grounds of defeat | unverified | Check Nyayasutra 5.2 and the Vadanyaya | data/debate_rules.json |
| 16 | Carvaka rejects inference as a pramana | unverified | Standard; Nagatomi p. 177 identifies a different doctrine, the "svabhavavada of the Lokayatas" (things are as they are by nature), so do not cite it for this | carvaka engine |

## What the Nagatomi thesis does not cover

It translates PV 2 (Pramanasiddhi) only. It cannot ground the core of the Dharmakirti engine, which lives in PV 1 (Svarthanumana) and its autocommentary, in the Hetubindu, and in the Nyayabindu. Its OCR text is also imperfect (diacritics are garbled), so quote numbers and verse numbers from it only after checking the page image.

## Research still needed, in priority order

1. PV 1 with PVSV, verses 1 to 10 and the passages on the three reasons and on anupalabdhi: Gnoli 1960 is the standard edition (listed at https://east.ikga.oeaw.ac.at/data/7/16/), and Hayes and Gillon 1991 (J. Indian Philosophy 19) introduces PVSV 1 to 10. A scan of Gnoli was circulated on the Indology list in Dec 2021 (https://list.indology.info/pipermail/indology/2021-December/055538.html).
2. Hetubindu (ed. Steinkellner 1967, as cited in other work) for rows 7, 9 and 11.
3. A second reader for Nyaya, Navya-Nyaya and Jain rows (12 to 14).
4. A passage pointer for every case in data/cases.json. Today none of the 13 cases has one.
