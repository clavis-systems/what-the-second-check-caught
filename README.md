# What the second check caught

A register of the problems that second checks raised in my research projects, which are run by AI agents.

I direct AI coding agents that write the code, run the measurements and draft the texts. Before I froze a plan or
published a result, a second AI system usually reviewed it. I kept every review. This repository logs each problem
those reviews raised: 444 rows from 71 review reports, written between 4 and 22 October 2026.

## The numbers

| | |
|---|---:|
| review reports | 71 |
| rows in the register | 444 |
| distinct problems (rows counted) | 422 |
| serious problems | 70 |

A problem is **serious** (severity `HIGH`) if it would have changed a conclusion, a frozen or published number, or the
main comparison of a study.

Where the 70 serious problems were caught: 40 before the plan was frozen, 26 after the data but before publication,
4 after publication. The 4 late ones are all in one repository (report `R62`). A check made 52 minutes after I
published it found them, and they were fixed.

| Kind of serious problem | n |
|---|---:|
| `CODE` code bugs that change results | 23 |
| `CLAIM` claims stronger than the data | 21 |
| `METH` flaws of method or design | 18 |
| `PROT` changes to a frozen plan that were not declared | 5 |
| `REPRO` reproducibility | 2 |
| `NUM` wrong numbers | 1 |

49 of the 70 were in research work (code, plans, analyses) and 21 in texts about it (READMEs, notes, emails, posts).
66 were fixed, 1 was rejected with a written reason, and for 3 I found no clear trace. Across all 422 problems, 92
have no clear trace of whether they were fixed. 355 of the 422 were raised by one reviewer, Codex.

Every figure above can be recomputed from the CSV files:

```
python summarise.py
```

## Files

| File | What it is |
|---|---|
| `register.csv` | one row per problem raised (444 rows): first the 290 rows with text, then the 154 withheld rows |
| `reports.csv` | the 71 review reports: date, reviewer, rows, SHA-256, public copy if there is one |
| `second_annotator.csv` | the 96 rows that a second annotator re-checked against the reports |
| `summarise.py` | recomputes the figures in this README (Python 3, standard library only) |

## Columns of `register.csv`

| Column | Meaning |
|---|---|
| `row_id` | row number in the original register |
| `annotation_pass` | `1` or `2`: the register was built in two passes on the same day |
| `project` | the project, by the name of its public repository; `not-yet-public-A` to `D` are explained below |
| `report_id` | the review report the row comes from (see `reports.csv`) |
| `review_round` | 1 for the first review of a document, 2 for the review of the corrected version, and so on |
| `date` | date of the review |
| `what_was_checked` | what the review looked at |
| `problem` | the problem raised, in English |
| `evidence_quote` | a short quote from the report that supports the row, in the language of the report (mostly Italian) |
| `evidence_quote_en` | English translation of the quote |
| `category`, `severity`, `stage`, `outcome` | see the definitions below |
| `work_type` | `research` (code, plans, analyses) or `text` (READMEs, notes, emails, posts) |
| `reviewer` | `Codex`, `independent recomputation` (a separate agent redid the analysis with its own code) or `separate Claude agent` |
| `duplicate_of` | if the same problem was already raised in an earlier row, that row |
| `counted` | `yes`, or why the row is not counted |
| `note` | how the outcome was decided: usually where the fix appears, with a quote. `[DOUBT]` marks a row where the annotator was unsure; `[OUTSIDE LIST]` marks a report that was not in the list first given to the annotator |
| `problem_it`, `note_it` | the original Italian text of the register, from which `problem` and `note` were translated |
| `text_withheld`, `withheld_sha256` | see "Rows whose text is withheld" |

## Definitions

- **category:** `NUM` wrong number or statistic; `METH` flaw of method or design; `CODE` bug that changes the results
  or makes the run fail; `PROT` the pre-registration or freeze was not respected, or a change was not declared; `CLAIM`
  a claim stronger than the data; `REPRO` reproducibility; `MINOR` form; `NONE` the report raised no problem.
- **severity:** `HIGH` would have changed a conclusion, a frozen or published number, or the main comparison; `MED`
  would have weakened a part or made it misleading; `LOW` cosmetic or an edge case.
- **stage:** `PRE_FREEZE` before the plan was frozen; `PRE_PUBLISH` after the data, before the material was published
  or sent; `POST_PUBLISH` the material was already public.
- **outcome:** `FIXED` if a later review round, a file or a commit shows the fix; `REJECTED` if it was rejected with a
  reason; `UNCLEAR` otherwise.
- **counted:** a row is counted once. Not counted: duplicates of an earlier row (17), rows for reports that raised no
  problem (4), and one row that the second annotator judged not to be an error of the work (row 79). Status updates
  in later rounds ("partly fixed", "still open") are not new rows.

## Rows whose text is withheld

For 154 rows the register keeps the counts and the labels, but not the text. 31 of the 70 serious problems are among
them.

- **146 rows, "not yet public":** the reviewed material is not public yet. `not-yet-public-A` is a competition entry that
  is not submitted yet; `not-yet-public-B` is a competition writeup that is submitted but not visible until the
  competition closes; `not-yet-public-C` is a study still running; `not-yet-public-D` is internal notes on ideas.
- **8 rows, "private correspondence":** reviews of an email to other researchers, and of a draft post and a short text
  for applications.

For these rows `withheld_sha256` is the SHA-256 of the original text, so any text released later can be checked
against it. The recipe is in `summarise.py` (function `withheld_sha256`): the compact JSON, with sorted keys and
without escaping non-ASCII characters, of `row_id`, `what_was_checked`, `problem`, `evidence_quote` and `note` in the
original Italian. I plan to release the text of the 146 "not yet public" rows when each project becomes public. The 8
rows of private correspondence stay withheld.

## Checking the rows

- When the register was built, a script checked that every quote is really in its report: 444 of 444.
- 32 of the 71 reports have a public copy (column `public_copy` in `reports.csv`): 23 are the identical file, and 9 are
  a copy that is not byte-identical but contains every quoted text. They cover 176 of the 444 rows.
- For the other reports, `reports.csv` gives the SHA-256 of the file, so a later release can be checked.

The four examples in my post are rows 53 (the census that counted the wrong thing), 206 (hidden tests that were not
hidden), 396 and 395 (the published 99.5% and the command that did not work, both in report `R62`). The temperature
example is row 2, whose text is withheld because that study is not public yet. The unsafe file lock is rows 444 and
13, also withheld. The 99.5% that was misread again and again appears for example in rows 378, 396 and 412.

## Second annotator

A second AI system (Codex) re-read the original reports for all the serious rows and for 25 rows picked at random among
the others (seeds 20261023 and 20261024): 96 rows in `second_annotator.csv`. The quote was there and said what the row
says in 96 of 96. It agreed on the severity in 95 and on the category in 95. It judged one row not to be an error of
the work. The three changes were adopted: row 43 from `HIGH` to `MED`, row 406 from `REPRO` to `MINOR`, row 79 not
counted.

This check covers all serious rows, but only 25 of the others. It does not confirm the totals or the share of each
kind.

## Limits

- Both annotators are AI systems.
- "Serious" is a judgement, and "one problem" depends on how a review is split into points. Other choices would change
  the totals.
- Most problems (355 of 422) were raised by one reviewer, Codex. So this measures mostly what that reviewer catches.
- For 92 of the 422 problems I found no clear trace of whether they were fixed.
- **Problems that no review caught are not here.** The real number of errors is higher, and I do not know by how much.
- All of this comes from one person's projects, over three weeks of reviews.
- The English text is a translation of the Italian register, made by AI agents and checked automatically for numbers.
  The Italian columns are the original.

## How this was made

I directed this work and checked the results. An AI agent (Claude) read the reviews and built the register, AI agents
translated it, another AI system (Codex) checked it, and Claude drafted this text. I decide what is published and I
answer for it.

## Licence

The data and the text (`register.csv`, `reports.csv`, `second_annotator.csv`, this README) are released under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). `summarise.py` is released under the Apache License 2.0
(`LICENSE`).

Emanuele Rizzan, independent researcher
