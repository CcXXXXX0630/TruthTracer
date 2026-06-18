<p align="right">
  <sub>Academic Risk Early-Warning System · v2.1</sub>
</p>

<p align="center">
  <a href="README_CN.md">🇨🇳 中文版</a>
</p>

# 🔍 TruthTracer

### *Don't ask whether a paper is fraudulent. Ask where the evidence stops supporting the claims.*

<br>

> **"The most damaging phrase in science isn't 'this is fraudulent' — it's 'the evidence for this claim stops here.'"**
>
> TruthTracer is an academic risk early-warning system. It does not declare papers "fraudulent" — it systematically audits research logic, data, statistics, citation networks, and reproducibility to pinpoint exactly where the evidence chain begins to break. Think of it as a reviewer, research integrity officer, and publisher investigator rolled into one.

<br>

---

### 🏗️ Three-Engine Architecture

<p align="center">
  <img src="https://img.shields.io/badge/methods-31-red?style=for-the-badge" alt="31 methods">
  <img src="https://img.shields.io/badge/engines-3-blue?style=for-the-badge" alt="3 engines">
  <img src="https://img.shields.io/badge/evidence-traceable-success?style=for-the-badge" alt="traceable">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="MIT">
</p>

```
     PAPER / AUTHOR / DATASET
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
  STATS    NETWORK    CASE
  Engine   Engine    Builder
  (21)     (10)      (scoring)
    │         │         │
    └─────────┼─────────┘
              ▼
   Risk Assessment Report
   (traceable evidence chain)
```

| Engine | Methods | What It Detects |
|:-------|:-------:|:----------------|
| **STATS** | 21 | Mathematical impossibilities in reported data (GRIM, Benford, p-curve, SPRITE, Statcheck...) |
| **NETWORK** | 10 | Open API scans: retraction rate, citation cartels, co-author closure, publication velocity... |
| **CASE** | — | Signal weighting + paper-type awareness + evidence chain generation |

<br>

---

### 📊 Risk Stratification

| Level | Criteria | Action |
|:------|:---------|:-------|
| 🔴 **CRITICAL** | ≥2 mathematical impossibilities | Escalate to ethics committee; request raw data |
| 🟠 **HIGH** | 1 impossibility OR multiple strong signals | Request raw data; flag for statistical review |
| 🟡 **MEDIUM** | Statistical anomalies, no impossibilities | Request clarification; cross-check supplements |
| 🟢 **LOW** | Minor pattern anomalies only | Standard peer review sufficient |
| ⚪ **CLEAN** | No concerning signals | Proceed with confidence |

> **The boundary between LOW and MEDIUM is the most important distinction this tool makes.**

<br>

---

### ✅ Live Test Validation

| Subject | Known Truth | TruthTracer Verdict |
|:--------|:------------|:-------------------|
| Yoshitaka Fujii | 183 retractions (most in history) | **HIGH RISK** — 21.4% retraction rate, 96 papers post-retraction |
| Frances Arnold | 2018 Nobel Prize, 4 self-retractions | MEDIUM RISK — self-retracted papers, continued publishing |
| Clean economics paper | No controversy | **LOW RISK** — auto-detected as "economic model", Benford discounted 70% |

<br>

---

### 🧬 RIGID Framework

Implements the [RIGID framework](https://doi.org/10.1016/j.eclinm.2024.102717) (Monash University, 2024):

| RIGID Principle | TruthTracer Implementation |
|:----------------|:--------------------------|
| Systematic assessment | 3 engines × 31 methods, fully automated |
| Multi-dimensional | Statistical + network + textual signals |
| Evidence traceability | Every RED FLAG → specific data point + method |
| Risk stratification | 5-tier system with paper-type context |
| Not a replacement for judgment | Every report states "Human judgment required" |

<br>

---

### ⚡ Quick Start

```bash
# 1. Statistical audit
python scripts/forensics.py audit --paper data.json > audit.json

# 2. Author investigation
python scripts/investigator.py investigate "Author Name" --deep > investigator.json

# 3. Evidence synthesis
python scripts/case_builder.py audit.json investigator.json \
    --text extracted_text.txt --output report.md
```

<p align="center">
  <b>29 of 31 methods use Python stdlib only — no pip install required.</b>
</p>

<br>

---

### 📁 Structure

```
TruthTracer/
├── scripts/
│   ├── forensics.py          ← 21 statistical checks (78 KB)
│   ├── investigator.py       ← 10 network signals (36 KB)
│   ├── case_builder.py       ← evidence chain builder (19 KB)
│   ├── extract_pdf.py        ← PDF text extraction
│   └── pysprite_vendor.py    ← GRIM + SPRITE implementation
├── examples/                    Sample audit reports
├── investigations/              Real case files
├── references/                  Method documentation
├── SKILL.md                     Hermes Agent definition
├── README.md                    English
├── README_CN.md                 Chinese
├── LICENSE                      MIT
└── CITATION.cff                 Citation metadata
```

---

### 📖 Cite

```bibtex
@software{TruthTracer,
  title = {TruthTracer: Academic Risk Early-Warning System},
  author = {CcXXXXX0630},
  year = {2026},
  url = {https://github.com/CcXXXXX0630/TruthTracer}
}
```

### 🙏 Acknowledgments

- RIGID framework: Monash University (2024), doi:10.1016/j.eclinm.2024.102717
- GRIM + SPRITE: adapted from QuentinAndre/pysprite (MIT)
- 29 of 31 methods are original implementations

### ⚠️ Disclaimer

TruthTracer outputs **risk signals**, not **verdicts**. All reports require human judgment.

---

<p align="center">
  <sub>MIT License · <a href="https://github.com/CcXXXXX0630">CcXXXXX0630</a></sub>
</p>
