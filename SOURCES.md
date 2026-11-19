# Sources

Everything below was found by web search on 19 Nov 2026. I could not download from the sandbox, so none of these files have been fetched or inspected. Open each one, read its header for the licence, and check the edition before you build on it. Some SARIT headers say "Availability: restricted", so check before redistributing any text.

## Start here (smallest corpus for a first paper)

| Text | Tradition | Where |
|---|---|---|
| Nyayasutra with Vatsyayana's Nyayabhasya | Nyaya | SARIT: https://sarit.indology.info/vatsyayana-nyayabhasya.xml?view=div (CC BY-SA 3.0 per header). Also in GRETIL via TextGrid: https://www.textgridrep.org/browse/48v3v.7 |
| Nyayasutra with Vacaspati's Tatparyatika (quotes Uddyotakara's Nyayavarttika) | Nyaya | SARIT: https://sarit.indology.info/nyayavarttikatatparyatika.xml?view=div |
| Nyayabindu with Dharmottara's Nyayabindutika and Durveka Misra's Dharmottarapradipa | Buddhist (Dharmakirti line) | SARIT: https://sarit.indology.info/dharmottarapradipa.xml?view=div (header says availability restricted) |
| Dharmottaratippanaka and Tarkarahasya (Yaita edition, Hetuvidya section) | Buddhist | SARIT: https://sarit.indology.info/dharmottaratippanaka.xml?view=div and https://sarit.indology.info/tarkarahasya.xml?view=div |
| Hemacandra, Pramanamimamsa with the author's vrtti | Jain | SARIT: https://sarit.indology.info/pramanamimamsa-and-vrtti.xml?view=div |
| Manikyanandi, Pariksamukha | Jain | Bibliotheca Indica edition (Vidyabhusana, 1909) on archive.org: https://ia800200.us.archive.org/34/items/Bibliotheca_Indica_Series/ParikshamukhaSutraOfManikyaNandi-SatishChandraVidyabhushana1909bis_text.pdf . English edition with notes (Ghoshal) on jainqq.org: https://jainqq.org/booktext/Parikshamukham_Romanized/004085 (pages marked for personal use, so do not redistribute) |
| Dignaga, Pramanasamuccaya chapter 1, hypothetical Sanskrit reconstruction (Steinkellner, 2005) | Buddhist | PDF: http://www.ikga.oeaw.ac.at/Mat/dignaga_PS_1.pdf (older link, may have moved). Bibliography of all editions: https://east.ikga.oeaw.ac.at/data/1/12/ |

## Portals and aggregators

- **GRETIL** (plain text and TEI, many Sanskrit texts including philosophy): https://gretil.sub.uni-goettingen.de/gretil.html . Cumulative download available. Licences vary by file.
- **SARIT** (TEI XML, EPUB, PDF, CC licensed): https://sarit.indology.info . Git repository: https://github.com/sarit/SARIT-corpus
- **pramana-nlp** (a corpus of Sanskrit pramana texts already cleaned for NLP, built from GRETIL and SARIT, with LDA experiments): https://www.github.com/tylergneill/pramana-nlp . Check this before cleaning anything yourself. It also mentions an intertextuality search tool at vatayana.info.
- **Virtual e-Text Archive of Indic Texts**, a directory that lists the Digital Corpus of Sanskrit, Hamburg CTS and others: https://indology.info/?p=89
- **Navya-Nyaya, Tattvacintamani**: a complete e-text exists from Central Sanskrit University (http://www.sanskrit.nic.in/DigitalBook/T/Tattvacintamani.pdf), made machine-searchable at https://github.com/sanskrit/raw_etexts/tree/master/nyAya-shAstram . Discussion on the Indology list (https://list.indology.info/pipermail/indology/2021-May/054799.html) notes that the underlying edition is undocumented, so treat it as a working text, not a critical edition.
- **Mimamsa**: Kumarila's Tantravarttika is on SARIT (https://sarit.indology.info/kumarila-tantravarttika.xml?view=div). For the Slokavarttika, the standard English translation is Ganganatha Jha (Bibliotheca Indica, 1900 to 1906). I did not confirm an open scan, so search archive.org.

## Tibetan side (needed for Dignaga and for checking Dharmakirti)

- Dignaga's Pramanasamuccaya survives complete only in two Tibetan translations, and the Sanskrit is partly reconstructed (OeAW research page: https://oeaw.ac.at/en/ikga/research/buddhist-studies/research-areas/pramanasamuccaya). Jinendrabuddhi's commentary has critical editions for chapters 1 and 2 in print.
- **BDRC / BUDA**: https://bdrc.io . E-texts can be downloaded as text files from the viewer, and custom dataset queries are supported. BDRC announced an open Tibetan Buddhist datasets for AI project in Feb 2026: https://www.bdrc.io/blog/2026/02/
- **BDRC Tibetan etext dump (April 2017)** on Zenodo, about 570 MB: https://zenodo.org/record/821218
- Caution: Zenodo also hosts a "Buddhist Classics AI Translation Series" with machine-made Tibetan, Chinese and English versions of the Tengyur (for example https://zenodo.org/records/17762001). Its own notes say the Sanskrit needs manual verification. Do not use it as ground truth.

## Print references to check your formalisation against

- Hattori, *Dignaga, On Perception* (Harvard Oriental Series 47), listed in the EAST bibliography above.
- Steinkellner and others on Jinendrabuddhi's Pramanasamuccayatika (OeAW).
- Phillips and Tatacharya, *Epistemology of Perception* (Tattvacintamani, perception chapter, 2004), and Phillips, a complete annotated translation of the Tattvacintamani (2020).
- Hemacandra, *Pramanamimamsa*, text and translation (Mookerjee), and Ghoshal's translation in the Jaina Gazette (https://jainqq.org/explore/034888/323).

## Pramanavarttika editions and secondary literature (added after reading Nagatomi)

Chapter order used by the OeAW EAST database: 1 svarthanumana, 2 pramanasiddhi, 3 pratyaksa, 4 pararthanumana (https://east.ikga.oeaw.ac.at/data/7/16/). That page lists the editions:

- Gnoli, R., *The Pramanavarttikam of Dharmakirti: The First Chapter with the Autocommentary* (Rome, 1960). The standard edition of PV 1 with PVSV. A scan was circulated on the Indology list: https://list.indology.info/pipermail/indology/2021-December/055538.html
- Miyasaka, Y., Pramanavarttika-Karika, Acta Indologica 2 (1971/72). Full verse text, Sanskrit and Tibetan.
- Sankrtyayana, R., 1938 edition, and Pandeya (ed.), 1989 (Motilal Banarsidass, with the autocommentary and Manorathanandin).
- Malvania, D., Svarthanumana-Parichchheda (Varanasi, 1959), listed at https://east.ikga.oeaw.ac.at/data/7/17/ .
- Hayes and Gillon 1991 (PVSV 1 to 10), and Hayes's 2008 translation of PVSV 11 to 38: https://www.unm.edu/%7Erhayes/pvsv_11-38.pdf
- Yaita 1985, "On Anupalabdhi: Annotated Translation of Dharmakirti's Pramanavarttikasvavrtti", listed at the EAST page above. Directly relevant to the `no-pot` case.
- Nagatomi, M., *A Study of Dharmakirti's Pramanavarttika: An English Translation and Annotation of the Pramanavarttika, Book I* (PhD thesis, Harvard University, 1957). Translates the Pramanasiddhi chapter (PV 2) only. Scan on the Internet Archive, OCR text is rough. It also contains a Tibetan-Sanskrit and Sanskrit-Tibetan index of that chapter, which could seed a terminology glossary. It is copyrighted, so keep it out of the repo.

## Not found

I did not confirm a standalone, openly downloadable Sanskrit e-text of Dharmakirti's Pramanavarttika or Hetubindu. SARIT's abbreviation tables show both are cited by the Dharmottara files, so look in pramana-nlp and in the SARIT file list first. Dharmakirti's Vadanyaya, Akalanka and Siddhasena are also unconfirmed.
