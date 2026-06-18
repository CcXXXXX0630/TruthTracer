<p align="right">
  <sub>Academic Risk Early-Warning System · v2.1</sub>
</p>

<p align="center">
  <a href="README_CN.md">中文版</a>
</p>

# TruthTracer

*The most damaging phrase in science isn't "this is fraudulent." It's "the evidence for this claim stops here."*

---

TruthTracer finds that boundary. It audits the logic, the numbers, the citation networks, the reproducibility — and flags where things stop adding up. It doesn't hand down verdicts. It builds evidence chains. Think reviewer meets research integrity officer meets publisher investigator, but in code.

---

## What's under the hood

Three engines. 31 methods. Zero API keys.

```
     PAPER / AUTHOR / DATASET
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
  STATS    NETWORK    CASE
  (21)     (10)     (scoring)
    │         │         │
    └─────────┼─────────┘
              ▼
   Risk report with traceable evidence
```

**Stats engine** (21 methods). Finds math that doesn't work — GRIM violations, Benford failures, p-curve clumping, SPRITE inconsistencies, statcheck mismatches. The kind of thing a sharp-eyed statistician catches at 2 AM during peer review.

**Network engine** (10 signals). Pulls from OpenAlex, CrossRef, PubMed. Retraction rates, citation rings, co-author closure, publication velocity. No API keys needed — just an internet connection.

**Case builder**. Combines signals with some common sense. Economic models get Benford checks discounted. Clinical trials get survival checks boosted. Two mathematical impossibilities = CRITICAL. Zero = ceiling at MEDIUM.

---

## How it classifies risk

| Level | What it means | What to do |
|:------|:--------------|:-----------|
| CRITICAL | At least 2 things that are mathematically impossible | Get the raw data. Now. |
| HIGH | 1 impossibility, or several strong signals | Request raw data. Flag for stats review. |
| MEDIUM | Anomalies, but nothing impossible | Ask the authors. Check the supplements. |
| LOW | Minor quirks | Peer review should catch these. |
| CLEAN | Nothing concerning | Move on. |

HIGH and MEDIUM are where this tool earns its keep. CRITICAL is rare — most papers with real problems land in HIGH.

---

## Real-world tests

We ran TruthTracer on three cases with known outcomes:

**Yoshitaka Fujii** — holds the record for most retractions in history (183). TruthTracer: HIGH RISK. 21.4% retraction rate, 96 papers published after his first retraction. The network engine caught what the stats engine couldn't: the post-retraction publishing pattern.

**Frances Arnold** — 2018 Nobel Prize in Chemistry. Four self-retracted papers. TruthTracer: MEDIUM RISK. Self-retraction is actually a positive signal — it means she caught her own errors. The tool correctly distinguished a fraudster from a scientist who made mistakes and owned them.

**Clean economics paper** — no controversy. TruthTracer: LOW RISK. Auto-detected as "economic model," automatically discounted the Benford check (economic data often follows power laws). No false alarm.

---

## Where this comes from

TruthTracer implements the [RIGID framework](https://doi.org/10.1016/j.eclinm.2024.102717) — a 2024 paper from Monash University that laid out five principles for research integrity auditing. All 31 methods map to one of the RIGID dimensions. 29 are original implementations. GRIM and SPRITE borrow from QuentinAndre/pysprite (MIT license).

---

## Quick start

```bash
# 1. Audit the numbers
python scripts/forensics.py audit --paper data.json > audit.json

# 2. Investigate the author
python scripts/investigator.py investigate "Author Name" --deep > investigator.json

# 3. Put it together
python scripts/case_builder.py audit.json investigator.json \
    --text extracted_text.txt --output report.md
```

29 of 31 methods run on Python stdlib. No pip install needed.

---

## Files

```
scripts/
  forensics.py           stats engine (78 KB)
  investigator.py        network engine (36 KB)
  case_builder.py        evidence chain builder (19 KB)
  extract_pdf.py         PDF text extraction
  pysprite_vendor.py     GRIM + SPRITE implementation
examples/                sample audit reports
investigations/          real case files
references/              methodology docs
```

---

## Cite

```bibtex
@software{TruthTracer,
  title = {TruthTracer: Academic Risk Early-Warning System},
  author = {CcXXXXX0630},
  year = {2026},
  url = {https://github.com/CcXXXXX0630/TruthTracer}
}
```

## Disclaimer

TruthTracer flags risks. It does not convict. Every report needs a human to read it.

---

<p align="center">
  <sub>MIT · <a href="https://github.com/CcXXXXX0630">CcXXXXX0630</a></sub>
</p>
