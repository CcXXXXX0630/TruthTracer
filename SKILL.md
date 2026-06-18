1|---
2|name: academic-data-forensics
3|description: >-
4|  Statistical forensic methods for detecting potential data fabrication in published
5|  research across ALL academic fields. 21 detection methods: Benford's Law, GRIM test,
6|  SPRITE reconstruction, p-curve analysis, statcheck (p-value verification against t/F/chi2),
7|  effect size consistency, scale boundary check, percentage sum check, correlation matrix
8|  positive-definiteness, ANOVA df consistency, duplicate number detection, rounding
9|  consistency, table-text cross-verification, count/survival data sanity, bootstrap audit,
- `journal-revision-workflow` — formula verification for self-revision (complementary: forensics audits others)
11|  sanity, and cross-group summary statistics consistency. Covers 7 domains: Psychology,
12|  Medicine/Epidemiology, Economics, Biology, Engineering/Environmental Science, Sociology,
13|  and universal methods. Integrated from QuentinAndre/pysprite (MIT, GRIM+SPRITE).
14|version: 1.1.0
15|metadata:
16|  hermes:
17|    tags:
18|      - forensics
19|      - statistics
20|      - academic-integrity
21|      - data-fabrication
22|      - fraud-detection
23|      - p-hacking
24|      - peer-review
25|      - cross-domain
26|    category: research
27|    related_skills: [chinese-academic-figures, journal-revision-workflow, humanizer-academic]
28|---
29|
30|# Academic Data Forensics Toolkit — Cross-Domain Edition
31|
32|Statistical forensic methods for detecting potential data fabrication in published research across ALL academic fields. 21 methods organized by domain applicability and runnable from a single JSON input.
33|
34|## When to Use
35|
36|- Auditing a suspicious paper's reported statistics before citing
37|- Pre-review data integrity screening as a journal editor
38|- Investigating potential p-hacking, impossible means, or fabricated sample sizes
39|- Verifying that reported test statistics match their p-values
40|- Checking if summary statistics are internally consistent across groups
41|- Cross-verifying numbers between tables and body text
42|
43|## Domain Coverage Matrix
44|
45|| # | Method | Psych | Med | Econ | Bio | Eng | Soc | All |
46||---|--------|:-----:|:---:|:----:|:---:|:---:|:---:|:---:|
47|| 1 | Benford's Law | | | Y | | | | Y |
48|| 2 | GRIM Test | Y | Y | Y | Y | | Y | |
49|| 3 | SPRITE Reconstruction | Y | Y | | | | Y | |
50|| 4 | Sample-Size Sanity | Y | Y | Y | Y | Y | Y | |
51|| 5 | p-curve Analysis | Y | Y | Y | Y | | Y | |
52|| 6 | Bootstrap Audit | Y | Y | Y | Y | Y | Y | |
53|| 7 | Mass Balance | | | | | Y | | |
| 8 | Formula Audit | | | | | Y | | |
55|| 9 | MC Parameter Sniff | | | | | Y | | |
56|| 10 | Digit Preference | | | | | | | Y |
57|| 11 | Stats Consistency | Y | Y | Y | Y | Y | Y | |
58|| 12 | Statcheck (p-value) | Y | Y | Y | Y | | Y | |
59|| 13 | Effect Size | Y | Y | Y | | | Y | |
60|| 14 | Scale Boundary | Y | Y | | | | Y | |
61|| 15 | Percentage Sum | Y | Y | Y | | | Y | Y |
62|| 16 | Correlation Matrix | Y | | Y | Y | | Y | |
63|| 17 | ANOVA df Check | Y | Y | Y | Y | | Y | |
64|| 18 | Duplicate Numbers | Y | Y | Y | Y | Y | Y | Y |
65|| 19 | Rounding Consistency | Y | Y | Y | Y | Y | Y | Y |
66|| 20 | Table-Text Consistency | Y | Y | Y | Y | Y | Y | Y |
67|| 21 | Count/Survival Data | | Y | | | | | |
68|
69|Psych=Psychology, Med=Medicine/Epi, Econ=Economics, Bio=Biology, Eng=Engineering/EnvSci, Soc=Sociology/Education, All=universal
70|
71|## Architecture (v2.0 — Three Engines)
72|
73|```
74|skill/
75|├── scripts/
76|│   ├── forensics.py          — Engine 1: Statistical (21 methods)
77|│   ├── investigator.py       — Engine 2: Non-Data Signals (6 methods)
78|│   └── case_builder.py       — Engine 3: Evidence Scoring + Report
79|├── references/
80|│   └── detection-playbook.md — Fraud taxonomy + workflows
81|└── templates/
82|    └── paper_data_template.json
83|```
84|
85|## Quick Start
86|
87|```bash
88|pip install pysprite numpy
89|
90|# Phase 1: Statistical audit
91|python scripts/forensics.py audit --paper paper_data.json > audit.json
92|
93|# Phase 2: Author investigation (requires internet; ~30 sec)
94|python scripts/investigator.py investigate "Author Name" > investigator.json
95|
96|# Phase 3: Case assembly
97|python scripts/case_builder.py audit.json investigator.json --output report.md
98|```
99|
100|## Method Catalog by Domain
101|
102|### Psychology / Social Sciences (14 methods)
103|GRIM, SPRITE, Sample-Size Sanity, p-curve, Stats Consistency, Statcheck, Effect Size, Scale Boundary, Percentage Sum, Correlation Matrix, ANOVA df, Duplicate Numbers, Rounding, Table-Text
104|
105|Key tell: Likert scale means outside [1,7], all SDs identical across groups, p-values clumped at 0.04-0.05.
106|
107|### Medicine / Epidemiology (13 methods)
108|GRIM, SPRITE, Sample-Size Sanity, p-curve, Stats Consistency, Statcheck, Effect Size, Scale Boundary, Percentage Sum, ANOVA df, Count/Survival, + universal
109|
110|Key tell: Events > at-risk, baseline imbalance in RCTs, rate per person-year inconsistent with raw counts.
111|
112|### Economics / Finance (10 methods)
113|Benford, GRIM, Sample-Size Sanity, p-curve, Stats Consistency, Statcheck, Percentage Sum, Correlation Matrix, + universal
114|
115|Key tell: First-digit violation, GDP shares not summing to 100%, impossible correlation matrices.
116|
117|### Biology / Genetics (10 methods)
118|GRIM, Sample-Size Sanity, p-curve, Stats Consistency, Statcheck, Correlation Matrix, ANOVA df, + universal
119|
120|Key tell: All SDs identical across treatment groups, equally spaced means (formula-generated), digit preference.
121|
122|### Engineering / Environmental Science (13 methods)
123|Mass Balance, Formula Formula, MC Parameter Sniff, Bootstrap Audit, Sample-Size Sanity, p-curve, Stats Consistency, Statcheck, + universal
124|
Checks reported vs correct formula derivation, identifies common unit-conversion inflation factors.
126|
127|### Universal (7 methods — work on ANY numeric data from ANY field)
128|Benford's Law, Digit Preference, Percentage Sum, Duplicate Numbers, Rounding Consistency, Table-Text Consistency, Full Audit
129|
130|## Method Details
131|
132|### 1. Benford's Law
133|First-digit distribution test. Natural data follows log distribution (30.1% start with 1, 4.6% with 9).
134|**Red flag**: MAD > 0.015 (non-conformity) or chi2 p < 0.05.
135|
136|### 2. GRIM Test (Granularity-Related Inconsistency of Means)
137|For integer-valued data reported to D decimal places with N participants, mean × N must be an integer.
138|**Red flag**: mean × N is not an integer → mathematically impossible.
139|
140|### 3. SPRITE (Sample Parameter Reconstruction)
141|Attempts to reconstruct raw distributions from (M, SD, N, scale range). If no valid distribution exists, the summary statistics are mutually impossible.
142|**Requires**: numpy + pysprite.
143|
144|### 4. Sample-Size Sanity
145|CV > 2.0, mean − 2×SD < 0 for non-negative data, all N are multiples of 10.
146|
147|### 5. p-curve Analysis
148|p-hacking detection via p-value distribution shape. Right-skewed = true effect; clumped at 0.04-0.05 = p-hacking.
149|**Red flag**: skew ratio < 1.0 or >40% of p-values in 0.04-0.05 bin.
150|
151|### 6. Bootstrap Audit
152|Parametric bootstrap: generates samples from reported parameters, checks if reported stats fall within bootstrap CIs.
153|
154|### 7. Mass Balance
155|Inputs = outputs + accumulation. Environmental engineering specific.
156|**Red flag**: relative imbalance exceeds tolerance (default 5%).
157|
### 8. Formula Audit
Checks reported vs correct formula derivation, identifies common unit-conversion inflation factors.
160|
161|### 9. MC Parameter Sniff
162|Normal on [0,1], Uniform not covering literature range, Triangular mode suspiciously central.
163|**Red flag**: 3+ suspicious parameter choices.
164|
165|### 10. Digit Preference
166|Terminal digits 0 and 5 over-preferred. Human-invented numbers favor round digits.
167|**Red flag**: 0+5 > 30% of terminal digits.
168|
169|### 11. Stats Consistency
170|All SDs identical across groups, all N multiples of 10, means equally spaced.
171|**Red flag**: 2+ patterns detected.
172|
173|### 12. Statcheck (p-value Verification)
174|Recomputes p from test statistic + df (t, F, chi2, Z) and compares to reported p.
175|**Red flag**: gross error (one significant, other not) or level mismatch.
176|
177|### 13. Effect Size Consistency
178|Cohen's d = (M1 − M2) / SD_pooled. Compares computed d to reported d.
179|**Red flag**: relative difference > 5%.
180|
181|### 14. Scale Boundary Check
182|Mean outside possible scale range, SD impossibly large for bounded scale.
183|**Red flag**: M=8.2 on 1-7 Likert or variance > (b−a)²/4.
184|
185|### 15. Percentage Sum Check
186|Subgroups not adding to 100%. All equal splits suspicious.
187|**Red flag**: sum deviation > 1pp + equal distribution pattern.
188|
189|### 16. Correlation Matrix Check
190|Symmetric, diagonal=1, values in [−1,1], positive semi-definite.
191|**Red flag**: r(A,B)=0.9, r(A,C)=0.9, r(B,C)=0.1 (mathematically impossible triangle).
192|
193|### 17. ANOVA df Check
194|df_between + df_within = N−1, df_between = k−1.
195|**Red flag**: df mismatch or F < 0.
196|
197|### 18. Duplicate Numbers
198|Same exact value appearing across independent series (copy-paste tell).
199|**Red flag**: ≥3 duplicates.
200|
201|### 19. Rounding Consistency
202|All values to same decimal places, impossible precision for instrument.
203|**Red flag**: all values to exactly 2dp or avg >5 significant figures.
204|
205|### 20. Table-Text Consistency
206|Same statistic reported differently in table vs body text.
207|**Red flag**: ≥2 mismatches.
208|
209|### 21. Count/Survival Data
210|Events > at-risk, rate inconsistent with person-years.
211|**Red flag**: any constraint violation.
212|
213|## Interpreting Results
214|
215|| RED FLAG Count | Verdict |
216||----------------|---------|
217|| 0 | CLEAN — No fabrication signal detected |
218|| 1 | SUSPICIOUS — Possible honest error; flag for closer reading |
219|| 2–3 | CRITICAL — Multiple independent signals converging |
220|| 4+ | LIKELY FABRICATED — Strong evidence of data manipulation |
221|
222|**Key principle**: A single RED FLAG could be an honest error. Multiple RED FLAGs across independent methods converging on the same conclusion is the gold standard for detection.
223|
224|## Paper Data JSON Format
225|
226|All fields optional — only tests with data will run. See `templates/paper_data_template.json` for a copy-paste template.
227|
228|## GitHub Provenance
229|
230|Exhaustive GitHub search (15+ queries) found only 2 relevant projects:
231|
232|| Source | Stars | Integration |
233||--------|-------|-------------|
234|| QuentinAndre/pysprite | 7 | Vendored: GRIM + SPRITE (`scripts/pysprite_vendor.py`) |
235|| kako-jun/lawkit | 8 | External: Rust CLI (Benford + Pareto + Zipf + outlier detection) |
236|
237|All other 19 methods are original implementations based on published methods.
238|
239|## Engine 2: Investigator (`scripts/investigator.py`)
240|
241|Non-data signal detectors using open APIs (OpenAlex, CrossRef, PubMed). No API keys required. Requires internet access.
242|
243|| Method | Signal | Key Discriminator |
244||--------|--------|-------------------|
245|| `retraction_proximity` | Retraction rate (retractions / total_works × 100) | **Strongest single signal**: 21.4% vs 0.4% = 50× (verified) |
246|| `post_retraction_publishing` | Papers published after first retraction | Ratio >0.5 + count >10 = RED FLAG |
247|| `publication_velocity_check` | >12 papers/year, output spikes | Use len() on peak_papers list (NOT raw comparison) |
248|| `affiliation_analysis` | Institution hopping, >4 countries | ≥5 institutions with <50% top-2 concentration |
249|| `self_citation_audit` | <1 citation/paper with >20 works | Low impact despite high volume = padding |
250|| `funding_transparency_check` | <10% papers report funding | Missing disclosures on empirical work |
251|
252|## Engine 3: Case Builder (`scripts/case_builder.py`)
253|
254|Combines Engine 1 + Engine 2 evidence into:
255|- Unified risk score (RED FLAG = 3pts, WARNING = 1pt)
256|- Risk level: LOW (0-5) / MEDIUM (6-12) / HIGH (13-20) / CRITICAL (21+)
257|- Professional Markdown investigation report with evidence table and recommendations
258|
259|## Dependencies
260|
261|- **Core (stdlib only)**: 19 of 21 methods
262|- **pysprite + numpy (pip)**: Methods 3 (SPRITE) + enhanced GRIM
263|
264|## Pitfalls
265|
266|1. **pysprite requires numpy** — SPRITE and enhanced GRIM are skipped with a clean message if numpy is missing. Install with `pip install numpy pysprite`.
267|2. **Statcheck distribution functions** — Uses numerical approximations (continued fraction, series expansion). For critical audits, cross-validate against R's `pt()`, `pf()`, `pchisq()`.
268|3. **ANOVA df check assumes simple designs** — Multi-factor or repeated-measures ANOVAs have complex df structures. The check flags potential issues but requires domain expertise to interpret.
269|4. **Correlation matrix positive-definiteness** limited to 3×3 determinant check. For larger matrices, verify eigenvalues independently.
270|5. **Table-text consistency requires manual data entry** — You must extract paired values from the paper. No automatic PDF parsing included.
271|6. **`works_count` retrieval (investigator)** — Do NOT use the search endpoint's `works_count`; it may be stale or omitted. Use the FULL author endpoint (`openalex_get_author`) or the retraction-filter endpoint's `meta.count` for accurate numbers. (Discovered during live testing vs Yoshitaka Fujii.)
272|7. **`peak_papers` is a list, not an int** — In `publication_velocity_check`, `sorted_years` returns `(year, list_of_works)` tuples. Always apply `len()` before comparing to thresholds. (Bug caught in smoke test.)
273|8. **Retraction rate, not raw count** — High-volume researchers may have retractions. Rate is the discriminator: Fujii=21.4% vs clean=0.4%. A researcher with 500 papers and 4 self-retractions is not suspicious.
274|9. **Post-retraction publishing false positives** — High-output honest researchers who self-retract a paper and continue their career will trigger on raw count. Use the ratio threshold (>0.5 AND >10) to reduce false positives. Cannot distinguish self-retraction from forced retraction without access to retraction notices.
275|10. **Investigator requires internet** — All API calls go to open endpoints (OpenAlex, CrossRef, PubMed). Offline mode returns clean errors. API calls are rate-limited at 10/sec.
276|11. **Live test validated discrimination**: Yoshitaka Fujii (known fraudster, 168 retractions): score=6 (HIGH) vs Frances Arnold (Nobel laureate, 4 self-retractions): score=3 (MEDIUM). Delta=3 confirms the toolkit discriminates correctly.
277|
278|## References
279|
280|- `references/detection-playbook.md` — Fraud taxonomy, investigation workflow, false positive patterns, and field-tested discriminator guidance.
281|- `templates/paper_data_template.json` — Copy-paste template for paper data input.
282|
283|### Method References
284|1. Benford, F. (1938). The law of anomalous numbers. *Proc. Am. Philos. Soc.*
285|2. Brown & Heathers (2017). The GRIM test. *Soc. Psychol. Personal. Sci.*
286|3. Heathers et al. (2018). SPRITE. *PeerJ*
287|4. Simonsohn et al. (2014). p-curve. *J. Exp. Psychol. Gen.*
288|5. Nuijten et al. (2016). statcheck. *Behav. Res. Methods*
289|6. Ioannidis (2005). Why most published research findings are false. *PLoS Med.*
290|
291|### GitHub Provenance
292|Exhaustive search (15+ queries) found 2 relevant projects:
293|- **QuentinAndre/pysprite** (★7, MIT) — Vendored as `scripts/pysprite_vendor.py`
294|- **kako-jun/lawkit** (★8) — External Rust CLI (Benford + Pareto + Zipf)
295|
296|All other methods are original implementations.
297|
298|## Related Skills
299|
300|- `chinese-academic-figures` — Monte Carlo parameter distribution guidance used by the MC sniff test
- `journal-revision-workflow` — formula verification for self-revision (complementary: forensics audits others)
302|- `humanizer-academic` — Academic prose de-AI-fication (forensics is for numbers, humanizer for text)
303|