1|<p align="right">
2|  <sub>Academic Risk Early-Warning System · v2.2</sub>
3|</p>
4|
5|<p align="center">
6|  <a href="README_CN.md">中文版</a>
7|</p>
8|
9|# TruthTracer
10|
11|*The most damaging phrase in science isn't "this is fraudulent." It's "the evidence for this claim stops here."*
12|
13|---
14|
15|TruthTracer finds that boundary. Seven detection engines. 30+ methods. One question: where does the evidence stop adding up?
16|
17|---
18|
19|## What's new in v2.2
20|
21|Four new engines. Name disambiguation for Chinese authors. Modular architecture — each engine runs standalone.
22|
23|| Engine | Methods | Finds |
24||--------|:------:|-------|
25|| **Stats** | 21 | Math that doesn't work — GRIM, Benford, p-curve, SPRITE, statcheck |
26|| **Network** | 10 | Retraction histories, citation cartels, paper mill signatures |
27|| **Text** | 6 | Tortured phrases (Cabanac 2023), AI-generated patterns, salami slicing |
28|| **Supplement** | 5 | Missing SI files, inaccessible data, unreproducible claims |
29|| **Citation** | 3 | References to retracted papers, fabricated citations, self-cite abuse |
30|| **Distribution** | 2 | Over/underdispersion, impossible variance homogeneity |
31|| **Preprint** | 2 | Outcome switching, abstract divergence from published version |
32|
33|The scorer fuses everything with paper-type awareness. Economic models get Benford discounted. Clinical trials get survival checks boosted. Review papers skip statistical tests entirely.
34|
35|---
36|
37|## Signal severity
38|
39|| Tier | Weight | Examples | What it means |
40||------|:------:|----------|---------------|
41|| CRITICAL | 3 pts | GRIM impossible, mean outside scale, events > at-risk | Mathematical impossibility. Near-certain fraud. |
42|| STRONG | 2 pts | Benford MAD>0.03, 10+ tortured phrases, retraction rate >10% | High suspicion. |
43|| MODERATE | 1 pt | Digit preference, SD homogeneity, 2+ tortured phrases | Worth a look. |
44|| WEAK | 0.5 pt | Rounding uniformity, 1 tortured phrase | Often a false positive. |
45|
46|Golden rule: zero CRITICAL signals caps risk at MEDIUM. Only mathematical impossibility proves near-certain fraud.
47|
48|---
49|
50|## Why name disambiguation matters
51|
52|A Chinese researcher named A common Chinese name can have 195 papers in OpenAlex. After TruthTracer filters by research domain, 124 remain. After domain filtering, unrelated papers from completely different fields are removed. Without this filter, 36% of the author profile was someone else's work. That level of contamination makes every network signal unreliable. TruthTracer fixes it before analysis starts.
53|
54|---
55|
56|## Tested on real cases
57|
58|| Subject | Known truth | Verdict | Key signal |
59||---------|------------|---------|------------|
60|| Known fraudster | 183 retractions | HIGH | Retraction rate 21.4% |
61|| Nobel laureate | 4 self-retractions | MEDIUM | 0.4%, all self-retractions |
62|| Clean economics paper | No controversy | LOW | Economic model → Benford downgraded |
63|| Retracted paper with collusion | Multiple authors | CRITICAL | Network engine caught collusion pattern |
64|| Clean LCA paper | No controversy | LOW | LCA model detected, correctly downgraded |
65|| Clean researcher with common name | Clean record | LOW | 0 retractions, 0 tortured phrases |
66|
67|---
68|
69|## Quick start
70|
71|```bash
72|# Full audit
73|python scripts/scorer.py --stats audit.json --network investigator.json --output report.md
74|
75|# Text check only (tortured phrases, AI patterns)
76|python scripts/text_engine.py check suspicious.txt
77|
78|# Author investigation
79|python scripts/network_engine.py investigate "Author Name" --deep
80|```
81|
82|---
83|
84|## Files
85|
86|```
87|scripts/
88|  scorer.py              evidence fusion + report generation
89|  stats_engine.py        21 statistical checks
90|  network_engine.py      10 author network signals
91|  text_engine.py         tortured phrases, AI patterns, salami slicing
92|  citation_engine.py     retracted refs, fabricated citations
93|  distribution_engine.py over/underdispersion detection
94|  preprint_engine.py     outcome switching, abstract divergence
95|  supplement_engine.py   SI completeness audit
96|  forensics.py           full stats engine (detailed)
97|  investigator.py        full network engine (detailed)
98|  case_builder.py        legacy case builder
99|  pysprite_vendor.py     GRIM + SPRITE (adapted from QuentinAndre/pysprite, MIT)
100|  extract_pdf.py         PDF text extraction
101|```
102|
103|---
104|
105|## Cite
106|
107|```bibtex
108|@software{TruthTracer,
109|  title = {TruthTracer: Academic Risk Early-Warning System},
110|  author = {CcXXXXX0630},
111|  year = {2026},
112|  version = {2.2.0},
113|  url = {https://github.com/CcXXXXX0630/TruthTracer}
114|}
115|```
116|
117|### Acknowledgments
118|
119|RIGID framework: Monash University (2024). Tortured phrases detection: adapted from Cabanac et al. (2021). GRIM + SPRITE: adapted from QuentinAndre/pysprite (MIT).
120|
121|### Disclaimer
122|
123|TruthTracer flags risks. It does not convict. Every report needs a human.
124|
125|---
126|
127|## Star History
128|
129|[![Star History Chart](https://api.star-history.com/svg?repos=CcXXXXX0630/TruthTracer&type=Date)](https://star-history.com/#CcXXXXX0630/TruthTracer&Date)
130|
131|---
132|
133|<p align="center">
134|  <sub>MIT · <a href="https://github.com/CcXXXXX0630">CcXXXXX0630</a></sub>
135|</p>
136|