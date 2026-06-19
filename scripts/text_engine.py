#!/usr/bin/env python3
"""
TruthTracer Text Engine — Tortured Phrases, AI Patterns, Salami Slicing
Based on: Cabanac et al. (2021), blader/humanizer 29 patterns, COPE guidelines
"""

import re
from collections import Counter
from typing import List, Dict
from difflib import SequenceMatcher

# ═══════════════ TORTURED PHRASES (cross-domain AI artifacts only) ═══════════════
TORTURED = {
    "flag to mean": "indicate/show",
    "colossal information": "big data",
    "counterfeit consciousness": "artificial intelligence",
    "human-made consciousness": "artificial intelligence",
    "irregular woods": "random forest",
    "backing vector machine": "support vector machine",
    "gradient dropping": "gradient descent",
    "brain network": "neural network",
    "profound learning": "deep learning",
    "regular language handling": "natural language processing",
    "picture acknowledgment": "image recognition",
    "discourse acknowledgment": "speech recognition",
    "vanishing slope": "vanishing gradient",
    "initiation work": "activation function",
    "misfortune work": "loss function",
    "grouping exactness": "classification accuracy",
    "mean square blunder": "mean squared error",
    "irregular backwoods": "random forest",
    "extraordinary inclination boosting": "extreme gradient boosting",
    "head part investigation": "principal component analysis",
    "straight relapse": "linear regression",
    "strategic relapse": "logistic regression",
    "choice tree": "decision tree",
    "information base": "database",
    "information index": "dataset",
    "information mining": "data mining",
    "distributed computing": "cloud computing",
    "web of things": "internet of things",
}

AI_PATTERNS = {
    "hedging_overload": [
        r"\b(it is (important|worth|necessary|essential|crucial|vital|critical) to (note|mention|highlight|emphasize))\b",
    ],
    "boilerplate_transitions": [
        r"\b(in (this|the present) (study|research|work|paper|investigation),? we)\b",
        r"\b(furthermore,?\s+(it is|\w+ (is|are|has|have)))\b",
    ],
    "significance_inflation": [
        r"\b(play(s|ed)? (a|an) (crucial|vital|pivotal|key|essential|important|significant|critical) role)\b",
        r"\b(of (great|paramount|utmost|crucial|vital) importance)\b",
        r"\b(has (attracted|garnered|drawn) (significant|considerable|widespread|growing|increasing) attention)\b",
    ],
}

def detect_tortured_phrases(text: str) -> dict:
    text_lower = text.lower()
    found = {p: {"count": len(re.findall(re.escape(p), text_lower))} for p in TORTURED}
    found = {k: v for k, v in found.items() if v["count"] > 0}
    total = sum(v["count"] for v in found.values())
    unique = len(found)
    
    if unique >= 10: risk, msg = "RED FLAG", f"Strong AI text evidence: {unique} tortured phrases"
    elif unique >= 5: risk, msg = "RED FLAG", f"Suspicious AI text: {unique} tortured phrases"
    elif unique >= 2: risk, msg = "WARNING", f"{unique} tortured phrases — may indicate AI paraphrasing"
    elif unique >= 1: risk, msg = "WARNING", "1 tortured phrase — isolated, possible translation error"
    else: risk, msg = "PASS", "No tortured phrases detected"
    
    return {"method": "Tortured Phrases (Cabanac 2023)", "total_hits": total,
            "unique_phrases": unique, "found": list(found.keys()), "verdict": risk, "message": msg}

def detect_ai_patterns(text: str) -> dict:
    counts = {cat: sum(len(re.findall(p, text, re.I)) for p in pats) for cat, pats in AI_PATTERNS.items()}
    total = sum(counts.values())
    issues = []
    if counts.get("hedging_overload", 0) > 10: issues.append(f"Excessive hedging ({counts['hedging_overload']})")
    if counts.get("boilerplate_transitions", 0) > 8: issues.append(f"Formulaic transitions ({counts['boilerplate_transitions']})")
    if counts.get("significance_inflation", 0) > 5: issues.append(f"Significance inflation ({counts['significance_inflation']})")
    
    risk = "RED FLAG" if total > 25 else "WARNING" if total > 12 else "PASS"
    return {"method": "AI Text Patterns", "total": total, "counts": counts, "issues": issues, "verdict": risk}

def salami_slicing_check(papers: List[dict]) -> dict:
    if len(papers) < 3: return {"verdict": "SKIP", "note": "Need >=3 papers"}
    issues = []
    similar = [(i,j,SequenceMatcher(None, papers[i].get('title','')[:100].lower(),
              papers[j].get('title','')[:100].lower()).ratio())
              for i in range(len(papers)) for j in range(i+1,len(papers))]
    high_sim = [(i,j,s) for i,j,s in similar if s > 0.7]
    if high_sim: issues.append(f"{len(high_sim)} highly similar title pairs — possible salami slicing")
    
    years = [p.get('year',0) for p in papers if p.get('year',0)]
    if years and max(years)-min(years) <= 3 and len(papers) >= 4:
        issues.append(f"{len(papers)} papers in {max(years)-min(years)} years — dataset fragmentation?")
    
    ns = [p.get('n',0) for p in papers if p.get('n',0)]
    if ns:
        top_n = Counter(ns).most_common(1)[0]
        if top_n[1] >= 3: issues.append(f"N={top_n[0]} repeated across {top_n[1]} papers")
    
    risk = "RED FLAG" if len(issues)>=2 else "WARNING" if issues else "PASS"
    return {"method": "Salami Slicing", "n_papers": len(papers), "issues": issues, "verdict": risk}

def full_text_audit(text: str) -> dict:
    r = {"tortured_phrases": detect_tortured_phrases(text), "ai_patterns": detect_ai_patterns(text)}
    words = len(text.split())
    sentences = len(re.findall(r'[.!?]+', text))
    if sentences > 20:
        avg = words/max(sentences,1)
        if 15 < avg < 18: r["sentence_uniformity"] = {"verdict": "WARNING", "message": f"Uniform sentence length ({avg:.0f}w) — AI text characteristic"}
    return r

if __name__ == '__main__':
    import sys, json
    if len(sys.argv) < 3: print("Usage: text_engine.py check <file>"); sys.exit(1)
    with open(sys.argv[2], 'r', encoding='utf-8') as f: text = f.read()
    print(json.dumps(full_text_audit(text), indent=2, ensure_ascii=False))
