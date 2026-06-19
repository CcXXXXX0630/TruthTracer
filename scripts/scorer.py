#!/usr/bin/env python3
"""
TruthTracer Scorer — Tiered Evidence Fusion + Report Generation
Paper-type-aware scoring with name disambiguation support.
"""

import json, os, re
from datetime import datetime
from typing import Dict, List

CRITICAL_KW = ["impossible", "outside scale", "events >", "negative", "triangle impossible", "df mismatch"]
STRONG_KW = ["benford non-conformity", "statcheck gross error", "p-curve left-skewed", "sprite failed",
             "tortured phrases", "retraction rate", "cartel", "closure ratio"]
MODERATE_KW = ["digit preference", "duplicate numbers", "sd identical", "percentage sum", "salami",
               "round n", "velocity", "self-citation"]

PAPER_TYPES = {
    "economic_model": {"kw": ["cost", "economic", "techno-economic", "lca", "scenario", "us$", "market"],
                       "discount": ["benford", "digit", "rounding"], "factor": 0.3,
                       "note": "Economic/LCA model: Benford/digit/rounding discounted (model parameters are human-chosen)"},
    "clinical": {"kw": ["patients", "clinical", "trial", "hazard ratio", "survival"],
                 "discount": [], "factor": 1.0, "boost": ["count", "statcheck"], "boost_factor": 1.5},
    "experimental": {"kw": ["experiment", "randomized", "p <", "t-test", "anova"], "discount": [], "factor": 1.0},
}
DEFAULT_TYPE = {"kw": [], "discount": [], "factor": 1.0, "note": "General paper: standard weighting"}

def detect_paper_type(paper_data: dict, text: str = "") -> str:
    combined = ((paper_data or {}).get('title', '') + ' ' + text).lower()
    scores = {t: sum(1 for kw in info['kw'] if kw in combined) for t, info in PAPER_TYPES.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] >= 2 else "general"

def classify_signal(verdict: str, method: str, issues: list = None) -> dict:
    combined = f"{verdict} {method} {' '.join(issues or [])}".lower()
    if any(kw in combined for kw in CRITICAL_KW): return {"tier": "CRITICAL", "weight": 3}
    if any(kw in combined for kw in STRONG_KW): return {"tier": "STRONG", "weight": 2}
    if any(kw in combined for kw in MODERATE_KW): return {"tier": "MODERATE", "weight": 1}
    if "RED FLAG" in verdict: return {"tier": "STRONG", "weight": 2}
    if "WARNING" in verdict: return {"tier": "MODERATE", "weight": 1}
    return {"tier": "PASS", "weight": 0}

def score(forensics: dict = None, investigation: dict = None, text_results: dict = None,
          paper_data: dict = None, text_sample: str = "") -> dict:
    ptype = detect_paper_type(paper_data, text_sample)
    adj = PAPER_TYPES.get(ptype, DEFAULT_TYPE)
    
    evidence, notes = [], []
    critical_n = strong_n = moderate_n = weak_n = 0
    total_weight = 0.0
    
    def process(source, method, verdict, issues=None):
        nonlocal critical_n, strong_n, moderate_n, weak_n, total_weight
        sig = classify_signal(verdict, method, issues)
        w = sig['weight']
        if method in adj.get('discount', []):
            w *= adj.get('factor', 1.0)
            notes.append(f"'{method}' discounted ({ptype}): {adj.get('note','')[:80]}")
        if method in adj.get('boost', []):
            w *= adj.get('boost_factor', 1.5)
        
        if sig['tier'] == 'CRITICAL': critical_n += 1
        elif sig['tier'] == 'STRONG': strong_n += 1
        elif sig['tier'] == 'MODERATE': moderate_n += 1
        elif sig['tier'] == 'WEAK': weak_n += 1
        total_weight += w
        evidence.append({"source": source, "method": method, "verdict": verdict, "tier": sig['tier'], "weight": w})
    
    if forensics:
        for method, result in forensics.get('results', {}).items():
            if isinstance(result, list):
                for item in result: process("stats", method, item.get('verdict',''), item.get('issues',[]))
            elif isinstance(result, dict) and 'verdict' in result:
                process("stats", method, result['verdict'], result.get('issues',[]))
    
    if investigation:
        for method, result in investigation.items():
            if isinstance(result, dict) and 'verdict' in result:
                process("network", method, result['verdict'], result.get('issues',[]))
    
    if text_results:
        for method, result in text_results.items():
            if isinstance(result, dict) and 'verdict' in result:
                process("text", method, result['verdict'], [result.get('message','')])
    
    # Risk determination (Golden Rule: 0 CRITICAL -> ceiling MEDIUM)
    if critical_n >= 2: risk, conf = "CRITICAL", "Multiple mathematical impossibilities"
    elif critical_n >= 1: risk, conf = "HIGH", "Mathematical impossibility detected"
    elif strong_n >= 2: risk, conf = "MEDIUM", "Multiple strong signals — investigate"
    elif total_weight >= 3: risk, conf = "LOW", "Minor patterns — likely benign"
    elif total_weight >= 1: risk, conf = "LOW", "Few weak signals — paper-type noise"
    else: risk, conf = "CLEAN", "No concerning signals"
    
    if critical_n == 0 and risk == "HIGH": risk, conf = "MEDIUM", conf + " (no impossibilities)"
    
    return {"paper_type": ptype, "adjustments": notes,
            "signals": {"critical": critical_n, "strong": strong_n, "moderate": moderate_n, "weak": weak_n},
            "score": round(total_weight, 1), "risk": risk, "confidence": conf, "evidence": evidence}

def report(scored: dict, paper_title: str = "Untitled", output: str = None) -> str:
    risk_map = {"CRITICAL": "CRITICAL", "HIGH": "HIGH", "MEDIUM": "MEDIUM", "LOW": "LOW", "CLEAN": "CLEAN"}
    s = scored['signals']
    
    lines = [
        f"# TruthTracer Investigation Report",
        f"", f"**Target**: {paper_title}",
        f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Paper Type**: {scored['paper_type'].replace('_',' ').title()}",
        f"", "---", "", "## Verdict",
        f"", f"**Risk Level: {risk_map.get(scored['risk'], 'UNKNOWN')}**",
        f"**Score: {scored['score']:.1f}** | **Confidence: {scored['confidence']}**",
        f"", f"| Tier | Count |", f"|------|-------|",
        f"| CRITICAL | {s['critical']} |", f"| STRONG | {s['strong']} |",
        f"| MODERATE | {s['moderate']} |", f"| WEAK | {s['weak']} |",
    ]
    
    if scored.get('adjustments'):
        lines += ["", "### Adjustments"]
        for n in scored['adjustments']: lines.append(f"- {n}")
    
    lines += ["", "---", "", "### Detailed Evidence", ""]
    for e in scored['evidence']:
        lines.append(f"- [{e['tier']}] **{e['method']}** ({e['source']}): {e['verdict']}")
    
    # Actions
    actions = {"CRITICAL": "ESCALATE to ethics committee immediately",
               "HIGH": "Request raw data from authors",
               "MEDIUM": "Request clarification on flagged items",
               "LOW": "Standard peer review sufficient",
               "CLEAN": "Proceed with confidence"}
    lines += ["", "---", "", "## Recommended Action", "", f"**{actions.get(scored['risk'], 'Review manually')}**"]
    lines += ["", "---", "", "*TruthTracer v2.2 — Screening tool. Human judgment required.*"]
    
    report_text = '\n'.join(lines)
    if output:
        os.makedirs(os.path.dirname(output) or '.', exist_ok=True)
        with open(output, 'w', encoding='utf-8') as f: f.write(report_text)
    return report_text

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2: print("Usage: scorer.py --stats f.json --network n.json --text t.json --output r.md")
    else: print("Use from Python: scorer.score(forensics, investigation, text_results)")
