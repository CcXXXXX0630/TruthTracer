# Medicine/Epidemiology Data Fabrication Patterns

## High-Priority Red Flags

1. **Events > at-risk** (Count/Survival #21)
   - 45 events in treatment arm of 40 patients

2. **Baseline imbalance in RCTs** (Stats Consistency #11)
   - Significant differences at baseline that shouldn't exist with randomization
   - All baseline p-values > 0.05 but suspiciously uniform (0.40-0.60)

3. **Impossible adverse event rates** (Percentage Sum #15)
   - AE percentages summing to >100%

4. **Survival curve inconsistencies** (Count/Survival #21)
   - KM curves crossing when reported HR < 1.0

5. **Sample size impossibilities** (Sample-Size Sanity #4)
   - SD so small that CV < 0.05 for biological measurements
   - All N are exact multiples of 10

## Domain-Specific Checks

6. **HR vs median survival mismatch** — HR=0.5 but median difference only 1 month
7. **OR vs RR implausibility** — OR=0.2 when baseline risk is 50%
8. **Dose-response anomalies** — Perfect linear dose-response with zero deviation

## Known Cases
- Fujii (2012): 172 retracted papers, impossible adverse event distributions
- Boldt (2011): Fabricated clinical trial data with impossible means
- Reuben (2010): Fabricated pain-medication trial data
