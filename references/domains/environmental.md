# Environmental Science/Engineering Data Fabrication Patterns

## High-Priority Red Flags

1. **Mass balance violation** (Mass Balance #7)
   - Inputs != outputs + accumulation beyond 5% tolerance

2. **CH4 formula missing VSS/DS factor** (CH4 Formula #8)
   - CH4 = DS * 1000 * eta_AD * k_CH4 (wrong, inflates by 1.54x)
   - CH4 = DS * 1000 * f_VS * eta_AD * k_CH4 (correct)

3. **Monte Carlo parameter implausibility** (MC Sniff #9)
   - Normal distribution on physically bounded [0,1] parameters
   - Uniform not covering literature range
   - Triangular mode at exact center (real rates are skewed)

4. **Bootstrap audit failure** (Bootstrap #6)
   - Reported stats outside bootstrap 95% CI

## Domain-Specific Checks

5. **COD imputation plausibility** — Default 350 mg/L when measured mean is 252
6. **Biogas yield range** — k_CH4 outside 0.30-0.40 Nm3/kgVS
7. **Emission factor consistency** — Different factors for same process in different sections
8. **Rank-order preservation** — Gini varies wildly when parameters should preserve ranking

## Known Cases
- Common in WWTP methane: deterministic CH4 overestimated by 1.54x
- MC convergence fraud: Gini stabilizes at 300 iterations but authors report 100
- Sensitivity analysis cherry-picking: reporting only convenient parameters
