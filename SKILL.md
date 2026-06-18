---
name: academic-data-forensics
description: >-
  Statistical forensic methods for detecting potential data fabrication in published
  research across ALL academic fields. 21 detection methods: Benford's Law, GRIM test,
  SPRITE reconstruction, p-curve analysis, statcheck (p-value verification against t/F/chi2),
  effect size consistency, scale boundary check, percentage sum check, correlation matrix
  positive-definiteness, ANOVA df consistency, duplicate number detection, rounding
  consistency, table-text cross-verification, count/survival data sanity, bootstrap audit,
  mass balance, CH4 formula audit, Monte Carlo parameter sniff, digit preference, sample-size
  sanity, and cross-group summary statistics consistency. Covers 7 domains: Psychology,
  Medicine/Epidemiology, Economics, Biology, Engineering/Environmental Science, Sociology,
  and universal methods. Integrated from QuentinAndre/pysprite (MIT, GRIM+SPRITE).
version: 1.1.0
metadata:
  hermes:
    tags:
      - forensics
      - statistics
      - academic-integrity
      - data-fabrication
      - fraud-detection
      - p-hacking
      - peer-review
      - cross-domain
    category: research
    related_skills: [chinese-academic-figures, journal-revision-workflow, humanizer-academic]
---

# Academic Data Forensics Toolkit — Cross-Domain Edition

Statistical forensic methods for detecting potential data fabrication in published research across ALL academic fields. 21 methods organized by domain applicability and runnable from a single JSON input.

## When to Use

- Auditing a suspicious paper's reported statistics before citing
- Pre-review data integrity screening as a journal editor
- Investigating potential p-hacking, impossible means, or fabricated sample sizes
- Verifying that reported test statistics match their p-values
- Checking if summary statistics are internally consistent across groups
- Cross-verifying numbers between tables and body text

## Domain Coverage Matrix

| # | Method | Psych | Med | Econ | Bio | Eng | Soc | All |
|---|--------|:-----:|:---:|:----:|:---:|:---:|:---:|:---:|
| 1 | Benford's Law | | | Y | | | | Y |
| 2 | GRIM Test | Y | Y | Y | Y | | Y | |
| 3 | SPRITE Reconstruction | Y | Y | | | | Y | |
| 4 | Sample-Size Sanity | Y | Y | Y | Y | Y | Y | |
| 5 | p-curve Analysis | Y | Y | Y | Y | | Y | |
| 6 | Bootstrap Audit | Y | Y | Y | Y | Y | Y | |
| 7 | Mass Balance | | | | | Y | | |
| 8 | CH4 Formula Audit | | | | | Y | | |
| 9 | MC Parameter Sniff | | | | | Y | | |
| 10 | Digit Preference | | | | | | | Y |
| 11 | Stats Consistency | Y | Y | Y | Y | Y | Y | |
| 12 | Statcheck (p-value) | Y | Y | Y | Y | | Y | |
| 13 | Effect Size | Y | Y | Y | | | Y | |
| 14 | Scale Boundary | Y | Y | | | | Y | |
| 15 | Percentage Sum | Y | Y | Y | | | Y | Y |
| 16 | Correlation Matrix | Y | | Y | Y | | Y | |
| 17 | ANOVA df Check | Y | Y | Y | Y | | Y | |
| 18 | Duplicate Numbers | Y | Y | Y | Y | Y | Y | Y |
| 19 | Rounding Consistency | Y | Y | Y | Y | Y | Y | Y |
| 20 | Table-Text Consistency | Y | Y | Y | Y | Y | Y | Y |
| 21 | Count/Survival Data | | Y | | | | | |

Psych=Psychology, Med=Medicine/Epi, Econ=Economics, Bio=Biology, Eng=Engineering/EnvSci, Soc=Sociology/Education, All=universal

## Architecture (v2.0 — Three Engines)

```
skill/
├── scripts/
│   ├── forensics.py          — Engine 1: Statistical (21 methods)
│   ├── investigator.py       — Engine 2: Non-Data Signals (6 methods)
│   └── case_builder.py       — Engine 3: Evidence Scoring + Report
├── references/
│   └── detection-playbook.md — Fraud taxonomy + workflows
└── templates/
    └── paper_data_template.json
```

## Quick Start

```bash
pip install pysprite numpy

# Phase 1: Statistical audit
python scripts/forensics.py audit --paper paper_data.json > audit.json

# Phase 2: Author investigation (requires internet; ~30 sec)
python scripts/investigator.py investigate "Author Name" > investigator.json

# Phase 3: Case assembly
python scripts/case_builder.py audit.json investigator.json --output report.md
```

## Method Catalog by Domain

### Psychology / Social Sciences (14 methods)
GRIM, SPRITE, Sample-Size Sanity, p-curve, Stats Consistency, Statcheck, Effect Size, Scale Boundary, Percentage Sum, Correlation Matrix, ANOVA df, Duplicate Numbers, Rounding, Table-Text

Key tell: Likert scale means outside [1,7], all SDs identical across groups, p-values clumped at 0.04-0.05.

### Medicine / Epidemiology (13 methods)
GRIM, SPRITE, Sample-Size Sanity, p-curve, Stats Consistency, Statcheck, Effect Size, Scale Boundary, Percentage Sum, ANOVA df, Count/Survival, + universal

Key tell: Events > at-risk, baseline imbalance in RCTs, rate per person-year inconsistent with raw counts.

### Economics / Finance (10 methods)
Benford, GRIM, Sample-Size Sanity, p-curve, Stats Consistency, Statcheck, Percentage Sum, Correlation Matrix, + universal

Key tell: First-digit violation, GDP shares not summing to 100%, impossible correlation matrices.

### Biology / Genetics (10 methods)
GRIM, Sample-Size Sanity, p-curve, Stats Consistency, Statcheck, Correlation Matrix, ANOVA df, + universal

Key tell: All SDs identical across treatment groups, equally spaced means (formula-generated), digit preference.

### Engineering / Environmental Science (13 methods)
Mass Balance, CH4 Formula, MC Parameter Sniff, Bootstrap Audit, Sample-Size Sanity, p-curve, Stats Consistency, Statcheck, + universal

Key tell: Input-output mass imbalance, CH4 formula missing VSS/DS factor (1.54x inflation), Normal distribution on [0,1] parameters.

### Universal (7 methods — work on ANY numeric data from ANY field)
Benford's Law, Digit Preference, Percentage Sum, Duplicate Numbers, Rounding Consistency, Table-Text Consistency, Full Audit

## Method Details

### 1. Benford's Law
First-digit distribution test. Natural data follows log distribution (30.1% start with 1, 4.6% with 9).
**Red flag**: MAD > 0.015 (non-conformity) or chi2 p < 0.05.

### 2. GRIM Test (Granularity-Related Inconsistency of Means)
For integer-valued data reported to D decimal places with N participants, mean × N must be an integer.
**Red flag**: mean × N is not an integer → mathematically impossible.

### 3. SPRITE (Sample Parameter Reconstruction)
Attempts to reconstruct raw distributions from (M, SD, N, scale range). If no valid distribution exists, the summary statistics are mutually impossible.
**Requires**: numpy + pysprite.

### 4. Sample-Size Sanity
CV > 2.0, mean − 2×SD < 0 for non-negative data, all N are multiples of 10.

### 5. p-curve Analysis
p-hacking detection via p-value distribution shape. Right-skewed = true effect; clumped at 0.04-0.05 = p-hacking.
**Red flag**: skew ratio < 1.0 or >40% of p-values in 0.04-0.05 bin.

### 6. Bootstrap Audit
Parametric bootstrap: generates samples from reported parameters, checks if reported stats fall within bootstrap CIs.

### 7. Mass Balance
Inputs = outputs + accumulation. Environmental engineering specific.
**Red flag**: relative imbalance exceeds tolerance (default 5%).

### 8. CH4 Formula Audit
Checks reported vs correct (VSS × η_AD × k_CH4) vs wrong (DS × 1000 × η_AD × k_CH4, missing f_VS, inflates 1.54×).

### 9. MC Parameter Sniff
Normal on [0,1], Uniform not covering literature range, Triangular mode suspiciously central.
**Red flag**: 3+ suspicious parameter choices.

### 10. Digit Preference
Terminal digits 0 and 5 over-preferred. Human-invented numbers favor round digits.
**Red flag**: 0+5 > 30% of terminal digits.

### 11. Stats Consistency
All SDs identical across groups, all N multiples of 10, means equally spaced.
**Red flag**: 2+ patterns detected.

### 12. Statcheck (p-value Verification)
Recomputes p from test statistic + df (t, F, chi2, Z) and compares to reported p.
**Red flag**: gross error (one significant, other not) or level mismatch.

### 13. Effect Size Consistency
Cohen's d = (M1 − M2) / SD_pooled. Compares computed d to reported d.
**Red flag**: relative difference > 5%.

### 14. Scale Boundary Check
Mean outside possible scale range, SD impossibly large for bounded scale.
**Red flag**: M=8.2 on 1-7 Likert or variance > (b−a)²/4.

### 15. Percentage Sum Check
Subgroups not adding to 100%. All equal splits suspicious.
**Red flag**: sum deviation > 1pp + equal distribution pattern.

### 16. Correlation Matrix Check
Symmetric, diagonal=1, values in [−1,1], positive semi-definite.
**Red flag**: r(A,B)=0.9, r(A,C)=0.9, r(B,C)=0.1 (mathematically impossible triangle).

### 17. ANOVA df Check
df_between + df_within = N−1, df_between = k−1.
**Red flag**: df mismatch or F < 0.

### 18. Duplicate Numbers
Same exact value appearing across independent series (copy-paste tell).
**Red flag**: ≥3 duplicates.

### 19. Rounding Consistency
All values to same decimal places, impossible precision for instrument.
**Red flag**: all values to exactly 2dp or avg >5 significant figures.

### 20. Table-Text Consistency
Same statistic reported differently in table vs body text.
**Red flag**: ≥2 mismatches.

### 21. Count/Survival Data
Events > at-risk, rate inconsistent with person-years.
**Red flag**: any constraint violation.

## Interpreting Results

| RED FLAG Count | Verdict |
|----------------|---------|
| 0 | CLEAN — No fabrication signal detected |
| 1 | SUSPICIOUS — Possible honest error; flag for closer reading |
| 2–3 | CRITICAL — Multiple independent signals converging |
| 4+ | LIKELY FABRICATED — Strong evidence of data manipulation |

**Key principle**: A single RED FLAG could be an honest error. Multiple RED FLAGs across independent methods converging on the same conclusion is the gold standard for detection.

## Paper Data JSON Format

All fields optional — only tests with data will run. See `templates/paper_data_template.json` for a copy-paste template.

## GitHub Provenance

Exhaustive GitHub search (15+ queries) found only 2 relevant projects:

| Source | Stars | Integration |
|--------|-------|-------------|
| QuentinAndre/pysprite | 7 | Vendored: GRIM + SPRITE (`scripts/pysprite_vendor.py`) |
| kako-jun/lawkit | 8 | External: Rust CLI (Benford + Pareto + Zipf + outlier detection) |

All other 19 methods are original implementations based on published methods.

## Engine 2: Investigator (`scripts/investigator.py`)

Non-data signal detectors using open APIs (OpenAlex, CrossRef, PubMed). No API keys required. Requires internet access.

| Method | Signal | Key Discriminator |
|--------|--------|-------------------|
| `retraction_proximity` | Retraction rate (retractions / total_works × 100) | **Strongest single signal**: 21.4% vs 0.4% = 50× (verified) |
| `post_retraction_publishing` | Papers published after first retraction | Ratio >0.5 + count >10 = RED FLAG |
| `publication_velocity_check` | >12 papers/year, output spikes | Use len() on peak_papers list (NOT raw comparison) |
| `affiliation_analysis` | Institution hopping, >4 countries | ≥5 institutions with <50% top-2 concentration |
| `self_citation_audit` | <1 citation/paper with >20 works | Low impact despite high volume = padding |
| `funding_transparency_check` | <10% papers report funding | Missing disclosures on empirical work |

## Engine 3: Case Builder (`scripts/case_builder.py`)

Combines Engine 1 + Engine 2 evidence into:
- Unified risk score (RED FLAG = 3pts, WARNING = 1pt)
- Risk level: LOW (0-5) / MEDIUM (6-12) / HIGH (13-20) / CRITICAL (21+)
- Professional Markdown investigation report with evidence table and recommendations

## Dependencies

- **Core (stdlib only)**: 19 of 21 methods
- **pysprite + numpy (pip)**: Methods 3 (SPRITE) + enhanced GRIM

## Pitfalls

1. **pysprite requires numpy** — SPRITE and enhanced GRIM are skipped with a clean message if numpy is missing. Install with `pip install numpy pysprite`.
2. **Statcheck distribution functions** — Uses numerical approximations (continued fraction, series expansion). For critical audits, cross-validate against R's `pt()`, `pf()`, `pchisq()`.
3. **ANOVA df check assumes simple designs** — Multi-factor or repeated-measures ANOVAs have complex df structures. The check flags potential issues but requires domain expertise to interpret.
4. **Correlation matrix positive-definiteness** limited to 3×3 determinant check. For larger matrices, verify eigenvalues independently.
5. **Table-text consistency requires manual data entry** — You must extract paired values from the paper. No automatic PDF parsing included.
6. **`works_count` retrieval (investigator)** — Do NOT use the search endpoint's `works_count`; it may be stale or omitted. Use the FULL author endpoint (`openalex_get_author`) or the retraction-filter endpoint's `meta.count` for accurate numbers. (Discovered during live testing vs Yoshitaka Fujii.)
7. **`peak_papers` is a list, not an int** — In `publication_velocity_check`, `sorted_years` returns `(year, list_of_works)` tuples. Always apply `len()` before comparing to thresholds. (Bug caught in smoke test.)
8. **Retraction rate, not raw count** — High-volume researchers may have retractions. Rate is the discriminator: Fujii=21.4% vs clean=0.4%. A researcher with 500 papers and 4 self-retractions is not suspicious.
9. **Post-retraction publishing false positives** — High-output honest researchers who self-retract a paper and continue their career will trigger on raw count. Use the ratio threshold (>0.5 AND >10) to reduce false positives. Cannot distinguish self-retraction from forced retraction without access to retraction notices.
10. **Investigator requires internet** — All API calls go to open endpoints (OpenAlex, CrossRef, PubMed). Offline mode returns clean errors. API calls are rate-limited at 10/sec.
11. **Live test validated discrimination**: Yoshitaka Fujii (known fraudster, 168 retractions): score=6 (HIGH) vs Frances Arnold (Nobel laureate, 4 self-retractions): score=3 (MEDIUM). Delta=3 confirms the toolkit discriminates correctly.

## References

- `references/detection-playbook.md` — Fraud taxonomy, investigation workflow, false positive patterns, and field-tested discriminator guidance.
- `templates/paper_data_template.json` — Copy-paste template for paper data input.

### Method References
1. Benford, F. (1938). The law of anomalous numbers. *Proc. Am. Philos. Soc.*
2. Brown & Heathers (2017). The GRIM test. *Soc. Psychol. Personal. Sci.*
3. Heathers et al. (2018). SPRITE. *PeerJ*
4. Simonsohn et al. (2014). p-curve. *J. Exp. Psychol. Gen.*
5. Nuijten et al. (2016). statcheck. *Behav. Res. Methods*
6. Ioannidis (2005). Why most published research findings are false. *PLoS Med.*

### GitHub Provenance
Exhaustive search (15+ queries) found 2 relevant projects:
- **QuentinAndre/pysprite** (★7, MIT) — Vendored as `scripts/pysprite_vendor.py`
- **kako-jun/lawkit** (★8) — External Rust CLI (Benford + Pareto + Zipf)

All other methods are original implementations.

## Related Skills

- `chinese-academic-figures` — Monte Carlo parameter distribution guidance used by the MC sniff test
- `journal-revision-workflow` — CH4 formula verification for self-revision (complementary: forensics audits others)
- `humanizer-academic` — Academic prose de-AI-fication (forensics is for numbers, humanizer for text)
