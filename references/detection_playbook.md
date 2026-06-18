# Academic Fraud Detection Playbook

Systematic guide for detecting research misconduct across all disciplines.  
Organized by fraud type, detection method, and signal strength.

## Fraud Taxonomy

### Type 1: Data Fabrication (Making up data)
**Signal strength**: Very strong (mathematical impossibility)

| Signal | Detection Method | Domain |
|--------|-----------------|--------|
| Mean x N not integer | GRIM Test (#2) | Psych, Med, Soc |
| Mean outside scale boundaries | Scale Boundary (#14) | Psych, Med |
| No valid distribution produces reported (M, SD) | SPRITE (#3) | Psych, Med |
| Events > at-risk in survival data | Count/Survival (#21) | Medicine |
| Input != output + accumulation | Mass Balance (#6) | Engineering |

### Type 2: Data Manipulation (Altering real data)
**Signal strength**: Strong (statistical anomaly)

| Signal | Detection Method | Domain |
|--------|-----------------|--------|
| First-digit distribution deviates from Benford | Benford (#1) | All |
| p-values clustered at 0.04-0.05 | p-curve (#5) | All empirical |
| Digit 0/5 over-represented | Digit Preference (#10) | All |
| All SDs identical across groups | Stats Consistency (#11) | All |

### Type 3: p-Hacking / Significance Fishing
**Signal strength**: Medium (requires pattern analysis)

| Signal | Detection Method | Domain |
|--------|-----------------|--------|
| p-curve left-skewed (more p~0.05 than p<0.01) | p-curve (#5) | All empirical |
| p-value doesn't match test statistic | Statcheck (#12) | All |
| Effect size inconsistent with M and SD | Effect Size (#13) | Psych, Med |
| Multiple tests but no correction | ANOVA df (#17) | All |

### Type 4: Paper Mills (Organized fraud rings)
**Signal strength**: Cumulative (multiple weak signals -> strong)

| Signal | Detection Method | Domain |
|--------|-----------------|--------|
| Closed co-author circle | Co-Author Closure | All |
| >12 papers/year sustained | Publication Velocity | All |
| All papers in same journal | Venue Concentration | All |
| Same numbers across independent papers | Duplicate Numbers (#18) | All |
| Impossible peer review timelines | Review Timeline | All |
| Co-authors with retractions | Retraction Proximity | All |

### Type 5: Citation Manipulation
**Signal strength**: Medium (detectable with graph analysis)

| Signal | Detection Method | Domain |
|--------|-----------------|--------|
| >40% self-citation rate | Self-Citation Audit | All |
| Mutual citation rings | Citation Cartel | All |
| Co-authors citing each other exclusively | Co-Author Closure | All |

### Type 6: Undisclosed Conflicts
**Signal strength**: Low individually, strong in aggregate

| Signal | Detection Method | Domain |
|--------|-----------------|--------|
| No funding disclosure on empirical work | Funding Transparency | All |
| Industry funding on pro-industry results | Funding Transparency | Med, Econ |
| Affiliation hopping | Affiliation Analysis | All |

## Investigation Workflow

### Phase 1: Statistical Triage (5 minutes)
Run the full statistical audit. If 0 RED FLAGs, low priority.  
If 2+ RED FLAGs, proceed to Phase 2.

```
python scripts/forensics.py audit --paper paper_data.json > audit.json
python scripts/forensics.py report --input audit.json
```

### Phase 2: Author Investigation (10-30 minutes)
Run investigator on the first and corresponding authors.

```
python scripts/investigator.py investigate "Author Name" --deep > investigator.json
```

### Phase 3: Case Assembly (5 minutes)
Combine all evidence into a single risk score and report.

```
python scripts/case_builder.py audit.json investigator.json --output final_report.md
```

### Phase 4: Human Review
- Review the generated report
- Cross-check flagged items against the original paper
- Determine if escalation to editor/institution is warranted

## Red Flag Weight Guide

| Weight | Examples |
|--------|----------|
| **3 pts** (Critical) | GRIM impossible, Benford non-conformity, p-value mismatch, scale boundary violation |
| **1 pt** (Warning) | Digit preference, high closure ratio, suspicious velocity, self-citation > 40% |

## Known False Positive Patterns

- Benford: Small N (<50), assigned numbers (IDs, zip codes), rounded data
- GRIM: Large N * items > 10^precision (always passes)
- p-curve: Small number of p-values (<4 significant)
- Duplicate Numbers: Standard scale values (e.g., "3" on a 1-5 Likert)
- Velocity: Large collaborations with many co-authors

## References

- Ioannidis JPA (2005). Why Most Published Research Findings Are False. *PLoS Med* 2(8): e124.
- Simonsohn U, Nelson LD, Simmons JP (2014). P-curve: A key to the file-drawer. *J Exp Psychol Gen* 143(2):534-47.
- Brown NJL, Heathers JAJ (2017). The GRIM Test. *Soc Psychol Personal Sci* 8(4):363-369.
- Nuijten MB et al. (2016). statcheck. *Behav Res Methods* 48:1205-1226.
- Heathers JAJ et al. (2018). SPRITE. *PeerJ Preprints* 6:e26968.
- COPE (2024). Flowcharts for handling research misconduct. https://publicationethics.org
