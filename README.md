<p align="right">
  <sub>Academic Risk Early-Warning System · v2.2</sub>
</p>

<p align="center">
  <a href="README_CN.md">中文版</a>
</p>

# TruthTracer

*The most damaging phrase in science isn't "this is fraudulent." It's "the evidence for this claim stops here."*

---

TruthTracer finds that boundary. Seven detection engines. 30+ methods. One question: where does the evidence stop adding up?

---

## What's new in v2.2

Four new engines. Name disambiguation for Chinese authors. Modular architecture — each engine runs standalone.

| Engine | Methods | Finds |
|--------|:------:|-------|
| **Stats** | 21 | Math that doesn't work — GRIM, Benford, p-curve, SPRITE, statcheck |
| **Network** | 10 | Retraction histories, citation cartels, paper mill signatures |
| **Text** | 6 | Tortured phrases (Cabanac 2023), AI-generated patterns, salami slicing |
| **Supplement** | 5 | Missing SI files, inaccessible data, unreproducible claims |
| **Citation** | 3 | References to retracted papers, fabricated citations, self-cite abuse |
| **Distribution** | 2 | Over/underdispersion, impossible variance homogeneity |
| **Preprint** | 2 | Outcome switching, abstract divergence from published version |

The scorer fuses everything with paper-type awareness. Economic models get Benford discounted. Clinical trials get survival checks boosted. Review papers skip statistical tests entirely.

---

## Signal severity

| Tier | Weight | Examples | What it means |
|------|:------:|----------|---------------|
| CRITICAL | 3 pts | GRIM impossible, mean outside scale, events > at-risk | Mathematical impossibility. Near-certain fraud. |
| STRONG | 2 pts | Benford MAD>0.03, 10+ tortured phrases, retraction rate >10% | High suspicion. |
| MODERATE | 1 pt | Digit preference, SD homogeneity, 2+ tortured phrases | Worth a look. |
| WEAK | 0.5 pt | Rounding uniformity, 1 tortured phrase | Often a false positive. |

Golden rule: zero CRITICAL signals caps risk at MEDIUM. Only mathematical impossibility proves near-certain fraud.

---

## Why name disambiguation matters

A Chinese researcher named A common Chinese name can have 195 papers in OpenAlex. After TruthTracer filters by research domain, 124 remain. After domain filtering, unrelated papers from completely different fields are removed. Without this filter, 36% of the author profile was someone else's work. That level of contamination makes every network signal unreliable. TruthTracer fixes it before analysis starts.

---

## Tested on real cases

| Subject | Known truth | Verdict | Key signal |
|---------|------------|---------|------------|
| Known fraudster | 183 retractions | HIGH | Retraction rate 21.4% |
| Nobel laureate | 4 self-retractions | MEDIUM | 0.4%, all self-retractions |
| Clean economics paper | No controversy | LOW | Economic model → Benford downgraded |
| Retracted paper with collusion | Multiple authors | CRITICAL | Network engine caught collusion pattern |
| Clean LCA paper | No controversy | LOW | LCA model detected, correctly downgraded |
| Clean researcher with common name | Clean record | LOW | 0 retractions, 0 tortured phrases |

---

## Quick start

```bash
# Full audit
python scripts/scorer.py --stats audit.json --network investigator.json --output report.md

# Text check only (tortured phrases, AI patterns)
python scripts/text_engine.py check suspicious.txt

# Author investigation
python scripts/network_engine.py investigate "Author Name" --deep
```

---

## Files

```
scripts/
  scorer.py              evidence fusion + report generation
  stats_engine.py        21 statistical checks
  network_engine.py      10 author network signals
  text_engine.py         tortured phrases, AI patterns, salami slicing
  citation_engine.py     retracted refs, fabricated citations
  distribution_engine.py over/underdispersion detection
  preprint_engine.py     outcome switching, abstract divergence
  supplement_engine.py   SI completeness audit
  forensics.py           full stats engine (detailed)
  investigator.py        full network engine (detailed)
  case_builder.py        legacy case builder
  pysprite_vendor.py     GRIM + SPRITE (adapted from QuentinAndre/pysprite, MIT)
  extract_pdf.py         PDF text extraction
```

---

## Cite

```bibtex
@software{TruthTracer,
  title = {TruthTracer: Academic Risk Early-Warning System},
  author = {CcXXXXX0630},
  year = {2026},
  version = {2.2.0},
  url = {https://github.com/CcXXXXX0630/TruthTracer}
}
```

### Acknowledgments

RIGID framework: Monash University (2024). Tortured phrases detection: adapted from Cabanac et al. (2021). GRIM + SPRITE: adapted from QuentinAndre/pysprite (MIT).

### Disclaimer

TruthTracer flags risks. It does not convict. Every report needs a human.

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=CcXXXXX0630/TruthTracer&type=Date)](https://star-history.com/#CcXXXXX0630/TruthTracer&Date)

---

<p align="center">
  <sub>MIT · <a href="https://github.com/CcXXXXX0630">CcXXXXX0630</a></sub>
</p>
