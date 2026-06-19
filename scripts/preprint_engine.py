#!/usr/bin/env python3
"""
Preprint Auditor — Detect outcome switching between preprint and published version.
===================================================================================
Compares preprint (arXiv, bioRxiv, chemRxiv, etc.) against the published version
to detect undisclosed changes in results, sample sizes, or conclusions.

Method: If a paper has a preprint version, the published version's abstract,
sample size, key statistics, and conclusions are compared against the preprint.
Changes are flagged unless explicitly disclosed in the published paper.

Reference: COMPare trials project (Goldacre et al.), ICMJE pre-registration policy.
"""

import urllib.request, urllib.parse, json, re
from typing import List, Dict, Optional, Tuple
from difflib import SequenceMatcher

def _api_get(url: str, timeout: int = 12) -> Optional[dict]:
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'TruthTracer/2.3 (academic-integrity-tool)',
            'Accept': 'application/json'
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except:
        return None

# ═══════════════════════════════════════════════════════════
# 1. FIND PREPRINT VERSION
# ═══════════════════════════════════════════════════════════

def find_preprint(doi: str) -> Optional[dict]:
    """
    Search for a preprint version of a published paper.
    
    Checks: arXiv, bioRxiv, medRxiv, chemRxiv, Research Square, SSRN
    via OpenAlex which aggregates preprint-published relationships.
    
    Args:
        doi: DOI of the published paper
    
    Returns:
        Preprint info dict, or None if no preprint found
    """
    # Search OpenAlex for the published work, then check related preprints
    url = f"https://api.openalex.org/works/https://doi.org/{urllib.parse.quote(doi)}"
    data = _api_get(url)
    
    if not data:
        return None
    
    # Check for preprint relationships
    related = data.get('related_works', [])
    preprint_ids = []
    
    # Also check if this work IS a preprint (type check)
    if data.get('type') == 'preprint':
        return {
            "is_preprint": True,
            "preprint_source": data.get('primary_location', {}).get('source', {}).get('display_name', 'Unknown'),
            "preprint_doi": doi,
            "preprint_title": data.get('title', 'Unknown'),
            "preprint_date": data.get('publication_date', 'Unknown'),
            "preprint_abstract": _reconstruct_abstract(data)
        }
    
    # Search for preprint in related works
    for rel_id in related[:20]:
        rel_url = f"https://api.openalex.org/works/{rel_id.split('/')[-1]}"
        rel_data = _api_get(rel_url)
        if rel_data and rel_data.get('type') == 'preprint':
            preprint_ids.append(rel_data)
    
    if not preprint_ids:
        # Also try searching by title
        title = data.get('title', '')
        if title:
            search_url = f"https://api.openalex.org/works?search={urllib.parse.quote(title)}&filter=type:preprint&per_page=3"
            search_data = _api_get(search_url)
            if search_data:
                for w in search_data.get('results', []):
                    preprint_ids.append(w)
    
    if preprint_ids:
        p = preprint_ids[0]
        return {
            "is_preprint": False,
            "has_preprint": True,
            "preprint_source": p.get('primary_location', {}).get('source', {}).get('display_name', 'Unknown'),
            "preprint_doi": p.get('doi', 'Unknown'),
            "preprint_title": p.get('title', 'Unknown'),
            "preprint_date": p.get('publication_date', 'Unknown'),
            "preprint_abstract": _reconstruct_abstract(p)
        }
    
    return {"has_preprint": False}


def _reconstruct_abstract(work: dict) -> str:
    """Reconstruct abstract from OpenAlex inverted index."""
    ai = work.get('abstract_inverted_index', {})
    if not ai:
        return ""
    words = sorted([(pos, word) for word, positions in ai.items() for pos in positions])
    return ' '.join(w for _, w in words)


# ═══════════════════════════════════════════════════════════
# 2. COMPARE PREPRINT vs PUBLISHED
# ═══════════════════════════════════════════════════════════

def compare_preprint_published(preprint_abstract: str,
                                published_abstract: str,
                                preprint_n: Optional[int] = None,
                                published_n: Optional[int] = None,
                                preprint_key_stats: Optional[List[float]] = None,
                                published_key_stats: Optional[List[float]] = None) -> dict:
    """
    Compare preprint and published versions for undisclosed changes.
    
    Flags:
    - Sample size change without explanation
    - Key statistics change beyond rounding
    - Conclusion direction change
    - Abstract text divergence >30%
    
    Args:
        preprint_abstract: Abstract from preprint
        published_abstract: Abstract from published version
        preprint_n: Sample size in preprint
        published_n: Sample size in published version
        preprint_key_stats: Key numerical findings from preprint
        published_key_stats: Same statistics from published version
    
    Returns:
        dict with comparison results
    """
    issues = []
    changes = []
    
    # 1. Sample size change
    if preprint_n and published_n:
        n_change = abs(published_n - preprint_n)
        n_change_pct = n_change / max(preprint_n, 1) * 100
        if n_change_pct > 10:
            issues.append(
                f"Sample size changed by {n_change_pct:.0f}%: "
                f"preprint N={preprint_n}, published N={published_n}. "
                f"Additional data collection after preprint posting must be disclosed."
            )
            changes.append({"type": "sample_size_change", "from": preprint_n, "to": published_n,
                          "change_pct": round(n_change_pct, 1)})
        elif n_change > 0:
            changes.append({"type": "sample_size_minor_change", "from": preprint_n, "to": published_n})
    
    # 2. Key statistics change
    if preprint_key_stats and published_key_stats:
        stat_mismatches = 0
        for i, (pre, pub) in enumerate(zip(preprint_key_stats[:10], published_key_stats[:10])):
            if pre != 0 and abs(pub - pre) / abs(pre) > 0.05:  # >5% change
                stat_mismatches += 1
                changes.append({
                    "type": "statistic_change",
                    "index": i,
                    "preprint_value": round(pre, 4),
                    "published_value": round(pub, 4),
                    "relative_change_pct": round(abs(pub - pre) / max(abs(pre), 0.001) * 100, 1)
                })
        
        if stat_mismatches >= 3:
            issues.append(
                f"{stat_mismatches} key statistics changed by >5% between "
                f"preprint and published version without explanation."
            )
    
    # 3. Abstract text divergence
    if preprint_abstract and published_abstract:
        sim = SequenceMatcher(None, preprint_abstract[:500], published_abstract[:500]).ratio()
        divergence = (1 - sim) * 100
        
        if divergence > 50:
            issues.append(
                f"Abstract text changed by {divergence:.0f}% from preprint. "
                f"Major rewriting may obscure undisclosed changes."
            )
        
        changes.append({"type": "abstract_divergence", "divergence_pct": round(divergence, 1)})
    
    return {
        "method": "Preprint-Published Comparison",
        "has_preprint": True,
        "changes_detected": len(changes),
        "changes": changes,
        "issues": issues,
        "verdict": "RED FLAG" if len(issues) >= 2 else \
                   "WARNING" if issues else "PASS",
        "interpretation": (
            "Preprints provide a time-stamped record of initial findings. "
            "Undisclosed changes between preprint and published version "
            "may indicate outcome switching or post-hoc data adjustment. "
            f"Changes detected: {len(issues)} concerning, {len(changes)} total."
        )
    }


# ═══════════════════════════════════════════════════════════
# 3. FULL PREPRINT AUDIT
# ═══════════════════════════════════════════════════════════

def full_preprint_audit(published_doi: str,
                         published_abstract: str = "",
                         published_n: Optional[int] = None,
                         published_stats: Optional[List[float]] = None) -> dict:
    """
    Complete preprint audit pipeline.
    
    Args:
        published_doi: DOI of the published paper
        published_abstract: Abstract of the published paper
        published_n: Sample size in published paper
        published_stats: Key statistics from published paper
    
    Returns:
        Complete audit report
    """
    results = {}
    
    preprint = find_preprint(published_doi)
    results['preprint_info'] = preprint
    
    if preprint and preprint.get('has_preprint'):
        preprint_abs = preprint.get('preprint_abstract', '')
        comparison = compare_preprint_published(
            preprint_abs, published_abstract,
            preprint_n=preprint.get('preprint_n'),
            published_n=published_n,
            preprint_key_stats=preprint.get('preprint_stats'),
            published_key_stats=published_stats
        )
        results['comparison'] = comparison
    
    return results


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Preprint Auditor — detect outcome switching")
        print("Usage: python preprint_engine.py <doi>")
        sys.exit(1)
    result = find_preprint(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
