# Academic Integrity Investigation Report

**Target**: Displacing fishmeal with protein derived from stranded methane (Nature Sustainability, 2022)
**Date**: 2026-06-18 23:29 UTC
**Classification**: CONFIDENTIAL — For Editor/Reviewer Use Only

---

## Executive Summary

### Overall Risk: 🟠 **HIGH** (Score: 16)

- **2** RED FLAGs detected
- **10** WARNINGs detected

> Strong evidence of irregularities. Recommend escalation to journal editor / institution.

## Evidence Summary

| # | Source | Method | Verdict | Detail |
|---|--------|--------|---------|--------|
| 1 | statistical | benford | 🔴 RED FLAG |  |
| 2 | statistical | digit_preference | 🔴 RED FLAG |  |
| 3 | statistical | grim | ✅ PASS — Mean is mathematically possible |  |
| 4 | statistical | grim | ✅ PASS — Mean is mathematically possible |  |
| 5 | statistical | grim | ✅ PASS — Mean is mathematically possible |  |
| 6 | statistical | sample_size_sanity | 🟡 WARNING | ['Coefficient of variation = 1.6 (>1.0, high variability)', 'Mean - 2*SD = -69.0 |
| 7 | statistical | sample_size_sanity | 🟡 WARNING | ['Coefficient of variation = 2.0 (>1.0, high variability)', 'Mean - 2*SD = -30.0 |
| 8 | statistical | sample_size_sanity | 🟡 WARNING | ['Coefficient of variation = 4.0 (>2.0, extremely high variability)', 'Mean - 2* |
| 9 | statistical | stats_consistency | 🟡 WARNING | ['3/3 sample sizes are multiples of 10. Possible fabrication.'] |
| 10 | statistical | percentage_sum | 🟡 WARNING | ['Percentages sum to 703.0%, expected 100.0% (deviation: +603.0pp)'] |
| 11 | statistical | duplicate_numbers | ✅ PASS | [] |
| 12 | statistical | rounding | 🟡 WARNING | ['All 13 values reported to exactly 0 decimal places — suspiciously uniform (rea |
| 13 | statistical | table_text | ✅ PASS | [] |
| 14 | investigator | El_Abbadi_retractions | ✅ PASS | [] |
| 15 | investigator | El_Abbadi_velocity | ✅ PASS | ['26 papers, peak 9 in 2024 — normal for early career'] |
| 16 | investigator | El_Abbadi_affiliations | 🟡 WARNING | ['21 institutions across 4 countries — broad collaboration network'] |
| 17 | investigator | El_Abbadi_selfcite | ✅ PASS | [] |
| 18 | investigator | El_Abbadi_funding | 🟡 WARNING | ['0% funding disclosure rate'] |
| 19 | investigator | Criddle_retractions | ✅ PASS | ['0 retractions out of 320 papers'] |
| 20 | investigator | Criddle_velocity | 🟡 WARNING | ['Peak 22 papers/year — high but normal for senior professor'] |
| 21 | investigator | Criddle_affiliations | 🟡 WARNING | ['62 institutions — extensive collaboration history'] |
| 22 | investigator | Criddle_selfcite | ✅ PASS | [] |

## Statistical Forensics Detail

### benford
**Verdict**: RED FLAG

- n: 66
- chi2: 27.05
- chi2_flag: red
- chi2_critical_05: 15.51
- mad: 0.0643
- mad_level: NON-CONFORMITY — POTENTIAL MANIPULATION
- mad_flag: red

### digit_preference
**Verdict**: RED FLAG

- decimal_place: 1
- n: 66
- chi2: 480.97
- zero_pct: 90.9
- five_pct: 0.0
- zero_five_combined_pct: 90.9
- expected_each_pct: 10.0
- flags: ['Digits 0+5 account for 91% (>30%, possible fabrication)', 'Digit distribution deviates from uniform (chi2=481.0, p<0.05)']

### stats_consistency
**Verdict**: WARNING

- n_groups: 3
- sd_cv: 0.825
- round_n_ratio: 3/3
- equal_spacing: False
- ⚠ 3/3 sample sizes are multiples of 10. Possible fabrication.

### percentage_sum
**Verdict**: WARNING

- label: Various reported percentages
- reported_percentages: [90, 70, 30, 17, 2, 33, 14, 72, 81, 35, 10, 45, 60, 15, 18, 50, 6, 5, 22, 28]
- total: 703
- expected: 100.0
- deviation: 603.0
- all_equal_split: False
- ⚠ Percentages sum to 703.0%, expected 100.0% (deviation: +603.0pp)

### duplicate_numbers
**Verdict**: PASS

- n_series: 2
- n_unique_values: 11
- n_duplicates: 0
- n_suspicious: 0
- suspicious_examples: {}
- common_increments: []

### rounding
**Verdict**: WARNING

- n_values: 13
- precision_distribution: {'0': 13}
- avg_significant_figures: 15.5
- ⚠ All 13 values reported to exactly 0 decimal places — suspiciously uniform (real data has variable precision)
- ⚠ Average 15.5 significant figures — implausibly precise for most instruments

### table_text
**Verdict**: PASS

- n_pairs: 2
- n_mismatches: 0
- mismatches: []

## Investigator Detail (Non-Data Signals)

**Target Author**: Sahar El Abbadi & Craig Criddle (Stanford University)
**Scan Depth**: Deep

- Red Flags: 0
- Warnings: 4
- Risk Score: 14.8%

### El_Abbadi_velocity
**Verdict**: PASS
- 26 papers, peak 9 in 2024 — normal for early career

### El_Abbadi_affiliations
**Verdict**: WARNING
- 21 institutions across 4 countries — broad collaboration network

### El_Abbadi_funding
**Verdict**: WARNING
- 0% funding disclosure rate

### Criddle_retractions
**Verdict**: PASS
- 0 retractions out of 320 papers

### Criddle_velocity
**Verdict**: WARNING
- Peak 22 papers/year — high but normal for senior professor

### Criddle_affiliations
**Verdict**: WARNING
- 62 institutions — extensive collaboration history

## Recommended Actions

1. Request raw data from authors before proceeding with review
2. Flag for statistical review by a qualified biostatistician
3. Check PubPeer and Retraction Watch for related reports

---

*Report generated by Academic Data Forensics Toolkit. This is a screening tool — human judgment is required for final determination.*