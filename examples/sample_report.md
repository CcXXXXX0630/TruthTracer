# Academic Data Forensics Audit Report

**Paper**: Sample Paper for Forensic Testing (2024)
**Timestamp**: 2026-06-18T21:26:57.116761

## Overall Verdict: **CRITICAL — Multiple red flags detected**

| Flag Level | Count |
|-----------|-------|
| RED FLAG | 3 |
| WARNING | 0 |
| PASS | 2 |

---
## Benford

**Verdict**: RED FLAG

- **n**: 50
- **chi2**: 17.39
- **chi2_flag**: red
- **chi2_critical_05**: 15.51
- **mad**: 0.0442
- **mad_level**: NON-CONFORMITY — POTENTIAL MANIPULATION
- **mad_flag**: red

| Digit | Observed | Expected | Obs% | Exp% |
|-------|----------|----------|------|------|
| 1 | 9 | 15.0 | 18.0% | 30.1% |
| 2 | 7 | 8.8 | 14.0% | 17.6% |
| 3 | 5 | 6.2 | 10.0% | 12.5% |
| 4 | 4 | 4.9 | 8.0% | 9.7% |
| 5 | 4 | 4.0 | 8.0% | 7.9% |
| 6 | 5 | 3.4 | 10.0% | 6.7% |
| 7 | 5 | 2.9 | 10.0% | 5.8% |
| 8 | 8 | 2.5 | 16.0% | 5.1% |
| 9 | 3 | 2.3 | 6.0% | 4.6% |

---
## Digit Preference

**Verdict**: PASS

- **decimal_place**: 1
- **n**: 50
- **chi2**: 7.2
- **zero_pct**: 0.0
- **five_pct**: 10.0
- **zero_five_combined_pct**: 10.0
- **expected_each_pct**: 10.0
- **flags**: []

---
## Grim

### Item 1: Group A

**Verdict**: PASS — Mean is mathematically possible
- **reported_mean**: 3.47
- **n**: 30
- **decimal_places**: 2
- **mean_times_n**: 104.10000000000001
- **nearest_integer**: 104
- **difference**: 0.1
- **is_consistent**: True
- **possible_total_counts**: [104]

### Item 2: Group B

**Verdict**: RED FLAG — Reported mean is mathematically IMPOSSIBLE for integer data with N=30
- **reported_mean**: 5.82
- **n**: 30
- **decimal_places**: 2
- **mean_times_n**: 174.60000000000002
- **nearest_integer**: 175
- **difference**: 0.4
- **is_consistent**: False
- **message**: Mean × N = 174.6000 is not an integer. The reported mean cannot arise from integer-valued data with N=30.

### Item 3: Group C

**Verdict**: RED FLAG — Reported mean is mathematically IMPOSSIBLE for integer data with N=30
- **reported_mean**: 7.15
- **n**: 30
- **decimal_places**: 2
- **mean_times_n**: 214.5
- **nearest_integer**: 214
- **difference**: 0.5
- **is_consistent**: False
- **message**: Mean × N = 214.5000 is not an integer. The reported mean cannot arise from integer-valued data with N=30.

---
## Sample Size Sanity

### Item 1: Group A

**Verdict**: PASS
- **mean**: 3.47
- **sd**: 1.21
- **n**: 30
- **sem**: 0.2209
- **ci_half_width_95**: 0.433
- **cv**: 0.35
- **lower_2sd**: 1.05
- **n_roundness**: exact multiple of 10
- **issues**: []

### Item 2: Group B

**Verdict**: PASS
- **mean**: 5.82
- **sd**: 1.19
- **n**: 30
- **sem**: 0.2173
- **ci_half_width_95**: 0.4258
- **cv**: 0.2
- **lower_2sd**: 3.44
- **n_roundness**: exact multiple of 10
- **issues**: []

### Item 3: Group C

**Verdict**: PASS
- **mean**: 7.15
- **sd**: 1.22
- **n**: 30
- **sem**: 0.2227
- **ci_half_width_95**: 0.4366
- **cv**: 0.17
- **lower_2sd**: 4.71
- **n_roundness**: exact multiple of 10
- **issues**: []

---
## Stats Consistency

**Verdict**: RED FLAG

- **n_groups**: 3
- **sd_cv**: 0.0103
- **round_n_ratio**: 3/3
- **equal_spacing**: False
- **issues**: ['SDs nearly identical across groups (CV=0.010). Suspicious uniformity.', '3/3 sample sizes are multiples of 10. Possible fabrication.']

---
## Pcurve

**Verdict**: RED FLAG

- **n_total**: 8
- **n_significant**: 8
- **bins**: {'p<0.01': 3, '0.01-0.02': 0, '0.02-0.03': 0, '0.03-0.04': 1, '0.04-0.05': 4}
- **skew_ratio**: 0.75
- **skew_verdict**: P-hacking suspected (left-skewed, p-values clumped near 0.05)
- **skew_flag**: red
- **clump_pct_04_05**: 50.0
- **clump_verdict**: RED FLAG: >40% of p-values in 0.04-0.05 bin

---
## Mass Balance

**Verdict**: PASS

- **system**: AD Reactor
- **total_input**: 1500
- **total_output**: 1450
- **accumulation**: 50
- **expected_output**: 1450
- **imbalance**: 0
- **relative_imbalance_pct**: 0.0
- **tolerance_pct**: 5.0
- **is_balanced**: True
