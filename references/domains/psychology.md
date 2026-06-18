# Psychology-Specific Data Fabrication Patterns

## High-Priority Red Flags

1. **Likert scale mean outside range** (Scale Boundary Check #14)
   - M=8.2 on 1-7 scale, M=0.8 on 1-5 scale
   - Most common in multi-item composites where fabricator miscalculates

2. **All SDs identical across groups** (Stats Consistency #11)
   - SD=1.21 for all 4 groups with different means
   - Real data: SD varies with mean (floor/ceiling effects)

3. **p-values clustered at 0.04-0.05** (p-curve #5)
   - >40% of significant p-values in 0.04-0.05 bin
   - Real data: right-skewed, more p<0.01 than p~0.04

4. **Impossible means** (GRIM #2)
   - M=3.47 with N=17 on integer scale -> impossible

5. **Impossible correlation triangles** (Correlation Matrix #16)
   - r(A,B)=0.9, r(A,C)=0.9, r(B,C)=0.1 (must be >= 0.62)

## Domain-Specific Checks

6. **Cronbach's alpha impossibilities** — Alpha < 0 or > 1; alpha=0.98 with 3 items
7. **Factor loading patterns** — All loadings exactly 0.00 or 1.00
8. **Manipulation check statistics** — Same F-value for different checks; all p=0.04-0.05

## Known Cases
- Stapel (2011): Fabricated means with suspiciously regular patterns across 50+ studies
- Smeesters (2014): Impossible means detected by GRIM test post-hoc
- Wansink (2017): p-hacking detected via p-curve analysis of 50+ papers
