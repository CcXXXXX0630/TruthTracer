---
name: truthtracer
description: >-
  Don't ask whether a paper is fraudulent. Ask where the evidence stops supporting 
  the claims. TruthTracer is an academic risk early-warning system that systematically 
  audits research logic, data, statistics, text integrity, citation networks, and 
  reproducibility — generating traceable evidence chains across 7 domains and 30+ 
  detection methods. RIGID-framework-inspired (Monash University, 2024).
version: 2.2.0
metadata:
  hermes:
    tags: [academic-integrity, fraud-detection, research-forensics, evidence-chain,
           risk-assessment, peer-review, systematic-audit, tortured-phrases,
           paper-mill-detection, name-disambiguation, cross-domain, RIGID-framework]
    category: research
---

# TruthTracer — Academic Risk Early-Warning System

> **Don't ask whether a paper is fraudulent. Ask where the evidence stops supporting the claims.**

像审稿人、科研诚信官和出版商调查员一样审查论文，发现隐藏的科研诚信风险。不是"鉴定论文是否造假"的二元分类器，而是通过系统审计研究逻辑、数据、统计、文本、引用网络和可重复性，识别证据链断裂点并生成可追溯证据的学术风险预警系统。

---

## Architecture

```
TruthTracer/
├── SKILL.md
├── scripts/
│   ├── scorer.py              ← Evidence fusion + report generation
│   ├── stats_engine.py        ← Statistical forensics (21 methods)
│   ├── network_engine.py      ← Author investigation (10 methods)
│   ├── text_engine.py         ← Text forensics (tortured phrases, AI patterns)
│   ├── citation_engine.py     ← Citation audit (retracted, fabricated, self-cite)
│   ├── distribution_engine.py ← Distribution patterns (dispersion, homogeneity)
│   ├── preprint_engine.py     ← Preprint-published comparison
│   ├── supplement_engine.py   ← Supplementary material audit
│   ├── forensics.py           ← Full 21-method stats engine (detailed)
│   ├── investigator.py        ← Full 10-signal network engine (detailed)
│   ├── case_builder.py        ← Legacy case builder (v2.1)
│   └── pysprite_vendor.py     ← GRIM+SPRITE (QuentinAndre/pysprite, MIT)
├── references/
│   └── detection_playbook.md  ← Fraud taxonomy + detection workflows
├── examples/
└── investigations/
```

## Seven Detection Engines

| Engine | File | Methods | What It Detects |
|--------|------|---------|-----------------|
| **Stats** | `stats_engine.py` | 21 | Mathematical impossibilities + statistical anomalies |
| **Network** | `network_engine.py` | 10 | Author retraction rates, citation cartels, paper mills |
| **Text** | `text_engine.py` | 6 | Tortured phrases (Cabanac 2023), AI patterns, salami slicing |
| **Supplement** | `supplement_engine.py` | 5 | SI completeness, cross-verification, data accessibility |
| **Citation** | `citation_engine.py` | 3 | Retracted references, fabricated citations, self-cite rate |
| **Distribution** | `distribution_engine.py` | 2 | Over/underdispersion, variance homogeneity excess |
| **Preprint** | `preprint_engine.py` | 2 | Preprint-published outcome switching, abstract divergence |
| **Scorer** | `scorer.py` | — | Tiered evidence fusion, paper-type context, report generation |

## Signal Severity Tiers

| Tier | Weight | Examples | Fraud Certainty |
|------|--------|----------|-----------------|
| **CRITICAL** | 3 pts | GRIM impossible, mean outside scale, events > at-risk, correlation triangle impossible | Mathematical impossibility — near-certain |
| **STRONG** | 2 pts | Benford non-conformity (MAD>0.03), statcheck gross error, 10+ tortured phrases, retraction rate >10% | Statistical/textual/network anomaly — high suspicion |
| **MODERATE** | 1 pt | Digit preference, duplicate numbers, SD homogeneity, 2+ tortured phrases | Pattern anomaly — worth investigating |
| **WEAK** | 0.5 pt | Rounding uniformity, funding disclosure, velocity, 1 tortured phrase | Minor concern — often false positive |

**Golden Rule**: 0 CRITICAL signals → risk ceiling at MEDIUM. Only mathematical impossibility is near-certain fraud proof.

## Risk Stratification

| Level | Criteria | Action |
|-------|----------|--------|
| **CRITICAL** | 2+ mathematical impossibilities | Escalate to ethics committee |
| **HIGH** | 1 impossibility OR multiple strong signals | Request raw data; statistical review |
| **MEDIUM** | Statistical/text anomalies, no impossibilities | Request clarification |
| **LOW** | Minor pattern anomalies | Standard peer review |
| **CLEAN** | No signals | Proceed with confidence |

## Paper-Type Awareness

| Type | Detection Keywords | Adjustment |
|------|-------------------|------------|
| `economic_model` | cost, techno-economic, scenario, LCA, US$ | Benford/digit/rounding → 30% weight |
| `clinical` | patients, trial, hazard ratio, survival | Count/survival → 150% weight |
| `experimental` | experiment, randomized, p <, t-test | Full weight on all tests |
| `review` | review, meta-analysis, systematic | Skip statistical tests |

## Name Disambiguation (v2.2)

Chinese common names cause 30-40% contamination in OpenAlex author profiles. TruthTracer filters by research domain keywords before analysis. Verified on Zhang Haihan (张海涵): 195→124 papers after filtering out 71 misattributed papers (chicken ovaries, carbon anodes, plant fungi).

## Key Findings from Live Testing

| Test Subject | Result | Key Signal |
|-------------|--------|------------|
| Yoshitaka Fujii (183 retractions) | **HIGH** | Retraction rate 21.4% |
| Frances Arnold (Nobel 2018) | MEDIUM | Retraction rate 0.4% (self-retractions) |
| Nature Sustainability SCP paper | **LOW** | Economic model → Benford downgraded |
| BT retracted paper #5 (Ashok Pandey et al.) | **CRITICAL** | 118 combined retractions across 8 authors |
| RCR sludge LCA paper | **LOW** | LCA model → Benford downgraded |
| Zhang Haihan (西安建大) | **LOW** | 0 retractions, 0 tortured phrases, 36% name contamination |

## Quick Start

```bash
# Full audit (all engines)
python scripts/scorer.py --stats audit.json --network investigator.json --output report.md

# Text-only check
python scripts/text_engine.py check "D:/papers/suspicious.txt"

# Author investigation
python scripts/network_engine.py investigate "Author Name" --deep

# Generate report
python scripts/scorer.py --stats audit.json --network investigator.json --output report.md
```

## References

- RIGID Framework: https://doi.org/10.1016/j.eclinm.2024.102717 (Monash University, 2024)
- Cabanac G et al. (2021). Tortured phrases. arXiv:2107.06751
- Nuijten MB et al. (2016). statcheck. Behav Res Methods
- Brown & Heathers (2017). The GRIM test. Soc Psychol Personal Sci
- Simonsohn et al. (2014). p-curve. J Exp Psychol Gen
- Heathers et al. (2018). SPRITE. PeerJ Preprints
- COPE (2024). Flowcharts for handling research misconduct
