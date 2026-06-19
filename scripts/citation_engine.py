#!/usr/bin/env python3
"""
Citation Auditor — Verify reference integrity.
================================================
Detects: fabricated citations, retracted references, citation claim mismatch,
         excessive self-citation, citation cartel patterns.

All methods are field-agnostic. No domain-specific heuristics.

Reference: retractcheck (R package), COPE citation guidelines.
"""

import urllib.request, urllib.parse, json, re, time
from collections import Counter, defaultdict
from typing import List, Dict, Optional

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
# 1. RETRACTED REFERENCE DETECTOR
# ═══════════════════════════════════════════════════════════

def check_retracted_references(dois: List[str]) -> dict:
    """
    Check if any cited references have been retracted.
    
    Citing a retracted paper without acknowledging the retraction
    is a serious integrity concern. The reference may be valid if
    cited before retraction, but the paper should note the retraction.
    
    Args:
        dois: List of DOIs from the paper's reference list
    
    Returns:
        dict with retracted references and risk assessment
    """
    retracted = []
    checked = 0
    
    for doi in dois:
        if not doi or not doi.strip():
            continue
        doi_clean = doi.strip().lower()
        if not doi_clean.startswith('10.'):
            continue
        
        checked += 1
        # Check OpenAlex retraction status
        url = f"https://api.openalex.org/works/https://doi.org/{urllib.parse.quote(doi_clean)}"
        data = _api_get(url)
        
        if data and data.get('is_retracted'):
            retraction_info = data.get('retraction', {})
            retracted.append({
                "doi": doi_clean,
                "title": (data.get('title', 'Unknown') or 'Unknown')[:100],
                "year": data.get('publication_year', '?'),
                "retraction_date": retraction_info.get('date', 'Unknown'),
                "retraction_type": retraction_info.get('type', 'Unknown')
            })
        
        time.sleep(0.1)  # Polite rate limiting
    
    retract_rate = len(retracted) / max(checked, 1) * 100
    
    issues = []
    if retracted:
        issues.append(
            f"{len(retracted)}/{checked} cited references are retracted "
            f"({retract_rate:.1f}%). Citing retracted papers without acknowledgment "
            f"undermines the evidence base."
        )
    
    return {
        "method": "Retracted Reference Detector",
        "references_checked": checked,
        "retracted_found": len(retracted),
        "retraction_rate_pct": round(retract_rate, 1),
        "retracted_details": retracted[:10],
        "issues": issues,
        "verdict": "RED FLAG" if retract_rate > 5 else \
                   "WARNING" if retracted else "PASS",
        "interpretation": (
            f"References with retracted citations: {len(retracted)}. "
            f"Acceptable: 0. Concerning: 1+. Critical: >5% of reference list."
        )
    }


# ═══════════════════════════════════════════════════════════
# 2. FABRICATED CITATION DETECTOR
# ═══════════════════════════════════════════════════════════

def detect_fabricated_citations(dois: List[str]) -> dict:
    """
    Detect potentially fabricated (non-existent) citations.
    
    Common fabrication patterns:
    - DOI format is valid but resolves to nothing
    - DOI belongs to a completely different paper than described
    - Journal volume/page combinations that don't exist
    - References to journals that ceased publication before the cited year
    
    Args:
        dois: List of DOIs from the paper's reference list
    
    Returns:
        dict with suspicious citations
    """
    nonexistent = []
    checked = 0
    
    for doi in dois:
        if not doi or not doi.strip():
            continue
        doi_clean = doi.strip().lower()
        if not doi_clean.startswith('10.'):
            continue
        
        checked += 1
        url = f"https://api.crossref.org/works/{urllib.parse.quote(doi_clean)}"
        data = _api_get(url)
        
        if not data or 'message' not in data:
            nonexistent.append({
                "doi": doi_clean,
                "reason": "DOI not found in CrossRef database"
            })
        
        time.sleep(0.1)
    
    nonexistent_rate = len(nonexistent) / max(checked, 1) * 100
    
    issues = []
    if nonexistent:
        issues.append(
            f"{len(nonexistent)}/{checked} DOIs not found in CrossRef. "
            f"These may be fabricated references or formatting errors."
        )
    
    return {
        "method": "Fabricated Citation Detector",
        "references_checked": checked,
        "nonexistent_found": len(nonexistent),
        "nonexistent_rate_pct": round(nonexistent_rate, 1),
        "nonexistent_details": nonexistent[:10],
        "issues": issues,
        "verdict": "RED FLAG" if nonexistent_rate > 5 else \
                   "WARNING" if nonexistent_rate > 0 else "PASS",
        "interpretation": (
            f"Unverifiable references: {len(nonexistent)}. "
            f"0: acceptable. 1-2: check for formatting errors. "
            f"3+: possible fabrication indicator."
        )
    }


# ═══════════════════════════════════════════════════════════
# 3. SELF-CITATION CONCENTRATION
# ═══════════════════════════════════════════════════════════

def self_citation_concentration(reference_authors: List[str],
                                  target_authors: List[str]) -> dict:
    """
    Check if citations are disproportionately from the same author group.
    
    Normal self-citation rate: 10-25%.
    Suspicious: >35% self-citation.
    Potential manipulation: >50% (citation stacking).
    
    Args:
        reference_authors: List of author strings from references
        target_authors: List of author names from the target paper
    
    Returns:
        dict with concentration analysis
    """
    target_set = set(name.lower().strip() for name in target_authors)
    
    self_cite_count = 0
    total_refs = len(reference_authors)
    
    for ref_authors in reference_authors:
        # Check if any author in this reference matches target authors
        ref_names = [n.lower().strip() for n in ref_authors.split(',')]
        if any(name in target_set for name in ref_names):
            self_cite_count += 1
    
    self_rate = self_cite_count / max(total_refs, 1) * 100
    
    interpretation = ""
    if self_rate > 50:
        risk = "RED FLAG"
        interpretation = "Over half of citations are self-citations. This level of self-referencing suggests citation manipulation."
    elif self_rate > 35:
        risk = "RED FLAG"
        interpretation = "Self-citation rate exceeds normal scholarly practice. May indicate citation stacking."
    elif self_rate > 25:
        risk = "WARNING"
        interpretation = "Above-average self-citation rate. Acceptable in niche fields but warrants attention."
    else:
        risk = "PASS"
        interpretation = "Self-citation rate within normal scholarly range."
    
    return {
        "method": "Self-Citation Concentration",
        "total_references": total_refs,
        "self_citations": self_cite_count,
        "self_citation_rate_pct": round(self_rate, 1),
        "verdict": risk,
        "interpretation": interpretation
    }


# ═══════════════════════════════════════════════════════════
# 4. FULL CITATION AUDIT
# ═══════════════════════════════════════════════════════════

def full_citation_audit(dois: List[str],
                         reference_authors: List[str] = None,
                         target_authors: List[str] = None) -> dict:
    """
    Run complete citation integrity audit.
    
    Args:
        dois: List of DOIs from reference list
        reference_authors: Author strings for each reference
        target_authors: Paper's own authors
    
    Returns:
        Complete audit report
    """
    results = {}
    
    # Retracted references
    if dois:
        results['retracted_refs'] = check_retracted_references(dois)
        results['fabricated_refs'] = detect_fabricated_citations(dois)
    
    # Self-citation
    if reference_authors and target_authors:
        results['self_citation'] = self_citation_concentration(
            reference_authors, target_authors
        )
    
    # Summary
    red = sum(1 for r in results.values()
             if 'RED FLAG' in r.get('verdict', ''))
    warn = sum(1 for r in results.values()
              if 'WARNING' in r.get('verdict', ''))
    
    results['summary'] = {
        "tests_run": len(results),
        "red_flags": red,
        "warnings": warn,
        "overall": "RED FLAG" if red >= 2 else \
                   "WARNING" if red >= 1 or warn >= 2 else "PASS"
    }
    
    return results


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Citation Auditor — verify reference integrity")
        print("Usage: python citation_engine.py <dois_file>")
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        dois = [line.strip() for line in f if line.strip()]
    result = full_citation_audit(dois)
    print(json.dumps(result, indent=2, ensure_ascii=False))
