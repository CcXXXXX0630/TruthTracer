# Sample Paper Data for Academic Data Forensics

This is an annotated example input file for the `academic-data-forensics` skill. Each section demonstrates one or more forensic tests.

## Fields

- `values`: Raw numeric values from the paper (used by Benford's Law + Digit Preference)
- `descriptives`: Summary statistics per group (used by GRIM + Sample-Size Sanity + Stats Consistency)
- `p_values`: Reported p-values from significance tests (used by p-curve Analysis)
- `mass_balance`: Input-output data for environmental systems (used by Mass Balance Check)
- `ch4_params`: Methane estimation parameters (used by CH4 Formula Audit)
- `mc_params`: Monte Carlo parameter distributions (used by MC Parameter Sniff)

## Sample Data

```json
{
  "title": "Example: WWTP Methane Recovery Study (2024)",
  "values": [
    12.5, 34.2, 67.8, 91.2, 15.3, 28.7, 45.6, 89.1, 23.4, 56.7,
    78.9, 11.2, 34.5, 67.1, 90.3, 14.8, 27.6, 43.2, 87.5, 21.9,
    54.3, 76.8, 9.7, 32.1, 65.4, 88.9, 13.6, 26.5, 41.8, 85.2,
    19.7, 52.8, 74.3, 8.9, 31.2, 63.7, 86.4, 12.1, 25.3, 40.6,
    84.1, 18.4, 51.6, 73.2, 7.8, 30.5, 62.1, 85.9, 11.8, 24.7
  ],
  "descriptives": [
    {"mean": 3.47, "sd": 1.21, "n": 30, "label": "Group A (Control)"},
    {"mean": 5.82, "sd": 1.19, "n": 30, "label": "Group B (Treatment 1)"},
    {"mean": 7.15, "sd": 1.22, "n": 30, "label": "Group C (Treatment 2)"}
  ],
  "p_values": [0.001, 0.042, 0.038, 0.049, 0.003, 0.046, 0.041, 0.008],
  "mass_balance": {
    "inputs": {"Feedstock (t/d)": 1000, "Process water (t/d)": 500},
    "outputs": {"Biogas (t/d)": 200, "Digestate (t/d)": 1250},
    "accumulation": 50,
    "tolerance": 0.05,
    "system_name": "Anaerobic Digestion Reactor"
  },
  "ch4_params": {
    "reported_ch4": 192500,
    "ds": 1000,
    "vss_ds_ratio": 0.65,
    "eta_ad": 0.55,
    "k_ch4": 0.35
  },
  "mc_params": [
    {"name": "eta_AD", "dist_type": "normal", "params": [0.55, 0.10], "physical_range": [0, 1]},
    {"name": "k_CH4", "dist_type": "triangular", "params": [0.30, 0.35, 0.40], "physical_range": [0.20, 0.45]},
    {"name": "COD_default", "dist_type": "normal", "params": [350, 50], "physical_range": [0, 1000]}
  ]
}
```

## Expected Audit Findings for This Sample

| Test | Expected Verdict | Why |
|------|-----------------|-----|
| Benford's Law | RED FLAG | MAD > 0.03, first-digit distribution deviates significantly |
| GRIM (Group A) | PASS | 3.47 × 30 = 104.1 ≈ 104, mathematically possible |
| p-curve | RED FLAG | 50% of p-values in 0.04-0.05 bin, left-skewed (skew_ratio < 1) |
| CH4 Formula | RED FLAG | Reported CH4 = 192,500 exactly matches wrong formula (missing VSS/DS factor) |
| MC Sniff | WARNING | Normal distribution on [0,1] parameter (eta_AD), should be Triangular |
| Stats Consistency | WARNING | SDs nearly identical across all 3 groups, all N are multiples of 10 |
| Digit Preference | PASS | 0+5 accounts for < 20% of terminal digits |
| Sample-Size Sanity | PASS | CV < 1.0, no negative lower bounds |

**Overall**: CRITICAL — 3+ RED FLAGs detected across independent tests.
