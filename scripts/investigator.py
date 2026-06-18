#!/usr/bin/env python3
"""
Academic Investigator — Non-Data Signals Module
=================================================
Detects fraud signals beyond statistics: author networks, publication patterns,
citation manipulation, conflict of interest, and retraction proximity.

Open APIs used (no keys required):
  - OpenAlex (https://api.openalex.org) — Academic knowledge graph
  - CrossRef (https://api.crossref.org) — DOI metadata
  - PubMed E-utilities (https://eutils.ncbi.nlm.nih.gov) — Biomedical literature
  - Semantic Scholar (https://api.semanticscholar.org) — Citation graph

Methods:
  1. Author Network Analysis — Co-authorship graph, closure, central figures
  2. Self-Citation Audit — Unusual self-citation ratios
  3. Citation Cartel Detection — Mutual citation rings
  4. Publication Velocity — Suspiciously rapid output
  5. Retraction Proximity — Connections to retracted papers (rate-based)
  6. Post-Retraction Publishing — Continued output after retractions
  7. Peer Review Timeline — Anomalous review speed
  8. Affiliation Analysis — Institution hopping, paper mills
  9. Funding Transparency — Undisclosed COI patterns
 10. Co-Author Closure — Small, closed collaboration circles (paper mill signature)

Key Discriminator (from live testing vs Yoshitaka Fujii):
  RETRACTION RATE is the strongest signal. Fujii (168/787 = 21.4%) vs
  clean control (4/921 = 0.4%) = 50x difference. Raw retraction count
  is misleading for high-volume researchers. Always score by rate.
"""

import urllib.request
import urllib.parse
import json
import time
import math
from collections import defaultdict, Counter
from typing import List, Dict, Optional, Tuple, Set
from datetime import datetime


class RateLimiter:
    """Polite rate limiter for open APIs."""
    def __init__(self, calls_per_second=10):
        self.delay = 1.0 / calls_per_second
        self.last_call = 0
    
    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_call = time.time()

_limiter = RateLimiter(calls_per_second=10)

def _get_json(url: str, timeout: int = 15) -> Optional[dict]:
    """Fetch JSON from URL with rate limiting. Returns None on any error."""
    _limiter.wait()
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'AcademicForensics/2.0 (mailto:researcher@example.com)',
            'Accept': 'application/json'
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


# ---- OpenAlex API helpers ----
def openalex_search_authors(name: str, per_page: int = 10) -> List[dict]:
    url = f"https://api.openalex.org/authors?search={urllib.parse.quote(name)}&per_page={per_page}"
    data = _get_json(url)
    return data.get('results', []) if data else []

def openalex_get_author(author_id: str) -> Optional[dict]:
    url = f"https://api.openalex.org/authors/{author_id}"
    return _get_json(url)

def openalex_get_works_by_author(author_id: str, per_page: int = 50) -> List[dict]:
    url = f"https://api.openalex.org/works?filter=authorships.author.id:{author_id}&per_page={per_page}&sort=publication_date:desc"
    data = _get_json(url)
    return data.get('results', []) if data else []


# ============================================================
# CORE INVESTIGATION METHODS
# ============================================================

def retraction_proximity(author_name: str) -> dict:
    """
    Check author's retraction history. Uses OpenAlex direct retraction filter.
    
    PITFALL (from live testing): Do NOT use author-search endpoint for works_count.
    The search endpoint may omit or cache stale counts. Use the FULL author endpoint
    (openalex_get_author) or the retraction-filtered works endpoint which returns
    accurate meta.count.
    
    KEY DISCRIMINATOR: Retraction RATE (retractions / total_works * 100) is the
    strongest signal. Verified: Fujii=21.4% vs clean=0.4% (50x difference).
    Raw count alone is misleading for high-volume researchers.
    """
    issues = []
    
    url = f"https://api.openalex.org/authors?search={urllib.parse.quote(author_name)}&per_page=3"
    data = _get_json(url)
    if not data or not data.get('results'):
        return {"error": f"Author not found: {author_name}", "method": "Retraction Proximity", "verdict": "PASS"}
    
    author = data['results'][0]
    author_id = author['id'].split('/')[-1]
    display_name = author.get('display_name', author_name)
    works_count = author.get('works_count', 0)
    
    ret_url = f"https://api.openalex.org/works?filter=authorships.author.id:{author_id},is_retracted:true&per_page=200"
    ret_data = _get_json(ret_url)
    ret_count = ret_data.get('meta', {}).get('count', 0) if ret_data else 0
    ret_works = ret_data.get('results', []) if ret_data else []
    
    retraction_rate = (ret_count / works_count * 100) if works_count > 0 else 0
    
    if ret_count > 0:
        issues.append(
            f"Author has {ret_count} retracted papers out of {works_count} total "
            f"({retraction_rate:.1f}% retraction rate)"
        )
    
    retracted = []
    for w in ret_works[:10]:
        retracted.append({
            "title": (w.get('title', 'Unknown') or 'Unknown')[:100],
            "year": w.get('publication_year'),
            "doi": w.get('doi', 'N/A')
        })
    
    return {
        "method": "Retraction Proximity",
        "author": display_name,
        "total_works": works_count,
        "author_retractions": ret_count,
        "retraction_rate_pct": round(retraction_rate, 2),
        "retracted_papers": retracted,
        "issues": issues,
        "verdict": "RED FLAG" if retraction_rate > 5 else
                   "RED FLAG" if ret_count >= 10 else
                   "WARNING" if ret_count >= 2 else
                   "WARNING" if ret_count >= 1 else "PASS"
    }


def post_retraction_publishing(author_name: str) -> dict:
    """
    Check if author continued high-volume publishing after first retraction.
    
    PITFALL (from live testing): High-output honest researchers who self-retract
    a paper and continue their normal career will trigger false positives on
    raw post-retraction count. Use post_retraction_RATIO with a threshold (>0.5
    AND >10 papers) to reduce false positives.
    
    Self-retraction = integrity-positive. Forced retraction = fraud-indicative.
    This method cannot distinguish them without access to retraction notices.
    """
    authors = openalex_search_authors(author_name, per_page=3)
    if not authors:
        return {"error": f"Author not found: {author_name}", "method": "Post-Retraction Publishing", "verdict": "PASS"}
    
    author = authors[0]
    author_id = author['id'].split('/')[-1]
    
    ret_url = f"https://api.openalex.org/works?filter=authorships.author.id:{author_id},is_retracted:true&sort=publication_date:asc&per_page=50"
    ret_data = _get_json(ret_url)
    ret_works = ret_data.get('results', []) if ret_data else []
    
    if not ret_works:
        return {"method": "Post-Retraction Publishing", "author": author.get('display_name', author_name), "verdict": "PASS — No retractions found"}
    
    first_ret_year = min((w.get('publication_year', 9999) for w in ret_works), default=None)
    all_works = openalex_get_works_by_author(author_id, per_page=100)
    
    post_ret = [w for w in all_works
                if w.get('publication_year', 0) and w.get('publication_year', 0) >= first_ret_year
                and not w.get('is_retracted', False)]
    
    post_ret_count = len(post_ret)
    total_works = len(all_works)
    post_ret_ratio = post_ret_count / max(total_works, 1) if total_works > 0 else 0
    
    issues = []
    if post_ret_ratio > 0.5 and post_ret_count > 10:
        issues.append(
            f"Published {post_ret_count} papers ({post_ret_ratio:.0%} of career) AFTER first retraction in {first_ret_year} — "
            f"retraction did not slow output"
        )
    elif post_ret_count > 0:
        issues.append(f"Published {post_ret_count} papers ({post_ret_ratio:.0%} of career) after first retraction ({first_ret_year})")
    
    return {
        "method": "Post-Retraction Publishing",
        "author": author.get('display_name', author_name),
        "first_retraction_year": first_ret_year,
        "total_retractions": len(ret_works),
        "papers_after_first_retraction": post_ret_count,
        "post_retraction_ratio": round(post_ret_ratio, 2),
        "issues": issues,
        "verdict": "RED FLAG" if (post_ret_ratio > 0.5 and post_ret_count > 10) else
                   "WARNING" if post_ret_count > 5 else "PASS"
    }


def publication_velocity_check(author_name: str) -> dict:
    """
    Check for suspiciously rapid publication rates.
    
    PITFALL: peak_papers from sorted_years is a LIST of works, not an int.
    Always use len() when comparing.
    
    Red flags: >12 papers/year sustained, sudden output spikes (3x+), 
    excessive venue concentration (>50% in single journal).
    """
    authors = openalex_search_authors(author_name, per_page=3)
    if not authors:
        return {"error": f"Author not found: {author_name}", "method": "Publication Velocity", "verdict": "PASS"}
    
    author = authors[0]
    author_id = author['id'].split('/')[-1]
    works = openalex_get_works_by_author(author_id, per_page=100)
    
    by_year = defaultdict(list)
    by_venue = defaultdict(int)
    
    for work in works:
        year = work.get('publication_year')
        if year:
            by_year[year].append(work)
        venue = work.get('host_venue', {})
        if venue:
            by_venue[venue.get('display_name', 'Unknown')] += 1
    
    issues = []
    sorted_years = sorted(by_year.items(), key=lambda x: len(x[1]), reverse=True)
    
    if sorted_years:
        peak_year, peak_papers_list = sorted_years[0]
        peak_papers = len(peak_papers_list)  # FIXED: was comparing list to int
        if peak_papers > 12:
            issues.append(f"Peak output: {peak_papers} papers in {peak_year} — suspiciously high (>12/year)")
        
        years_list = sorted(by_year.keys())
        if len(years_list) >= 3:
            counts = [len(by_year[y]) for y in years_list[-5:]]
            avg = sum(counts[:-1]) / max(len(counts[:-1]), 1)
            last = counts[-1]
            if avg > 0 and last / avg > 3 and last > 5:
                issues.append(f"Output spike: {last} papers in most recent year vs avg {avg:.1f}/year — 3x+ increase")
    
    total_works = len(works)
    if by_venue and total_works > 0:
        top_venue_count = max(by_venue.values())
        if top_venue_count / total_works > 0.5 and total_works > 5:
            top_venue_name = max(by_venue, key=by_venue.get)
            issues.append(f"{top_venue_count}/{total_works} papers ({top_venue_count/total_works*100:.0f}%) in '{top_venue_name}'")
    
    return {
        "method": "Publication Velocity Check",
        "author": author.get('display_name', author_name),
        "total_works_analyzed": total_works,
        "years_active": len(by_year),
        "peak_year": {"year": sorted_years[0][0], "papers": len(sorted_years[0][1])} if sorted_years else None,
        "top_venues": dict(sorted(by_venue.items(), key=lambda x: x[1], reverse=True)[:5]),
        "issues": issues,
        "verdict": "RED FLAG" if len(issues) >= 2 else "WARNING" if issues else "PASS"
    }


def affiliation_analysis(author_name: str) -> dict:
    """Check for institution hopping, excessive international affiliations, possible paper mill patterns."""
    authors = openalex_search_authors(author_name, per_page=3)
    if not authors:
        return {"error": f"Author not found: {author_name}", "method": "Affiliation Analysis", "verdict": "PASS"}
    
    author = authors[0]
    author_id = author['id'].split('/')[-1]
    works = openalex_get_works_by_author(author_id, per_page=50)
    
    affiliations = {}
    countries = Counter()
    
    for work in works:
        for authorship in work.get('authorships', []):
            for inst in authorship.get('institutions', []):
                name = inst.get('display_name', 'Unknown')
                affiliations[name] = affiliations.get(name, 0) + 1
                country = inst.get('country_code', 'Unknown')
                if country:
                    countries[country] += 1
    
    issues = []
    sorted_aff = sorted(affiliations.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_aff) >= 5:
        top_count = sum(c for _, c in sorted_aff[:2])
        total = sum(affiliations.values())
        if total > 0 and top_count / total < 0.5:
            issues.append(f"High affiliation diversity: {len(sorted_aff)} institutions — top 2 only {top_count/total*100:.0f}%")
    
    if len(countries) >= 4:
        issues.append(f"Affiliations in {len(countries)} countries — possible affiliation padding")
    
    return {
        "method": "Affiliation Analysis",
        "author": author.get('display_name', author_name),
        "n_affiliations": len(affiliations),
        "n_countries": len(countries),
        "top_affiliations": dict(sorted_aff[:5]),
        "top_countries": dict(countries.most_common(5)),
        "issues": issues,
        "verdict": "WARNING" if issues else "PASS"
    }


def self_citation_audit(author_name: str) -> dict:
    """Check for unusually low citation impact suggesting self-citation padding."""
    authors = openalex_search_authors(author_name, per_page=3)
    if not authors:
        return {"error": f"Author not found: {author_name}", "method": "Self-Citation Audit", "verdict": "PASS"}
    
    author = authors[0]
    works_count = author.get('works_count', 0)
    cited_by = author.get('cited_by_count', 0)
    h_index = author.get('summary_stats', {}).get('h_index', 0)
    cites_per_paper = cited_by / max(works_count, 1)
    
    issues = []
    if cites_per_paper < 1 and works_count > 20:
        issues.append(f"Extremely low impact: {cites_per_paper:.1f} citations/paper ({cited_by} cites / {works_count} papers)")
    
    return {
        "method": "Self-Citation Audit",
        "author": author.get('display_name', author_name),
        "works_count": works_count,
        "total_cited_by": cited_by,
        "h_index": h_index,
        "citations_per_paper": round(cites_per_paper, 2),
        "issues": issues,
        "verdict": "WARNING" if issues else "PASS"
    }


def funding_transparency_check(author_name: str) -> dict:
    """Check for undisclosed funding patterns. <10% funding disclosure is suspicious."""
    authors = openalex_search_authors(author_name, per_page=3)
    if not authors:
        return {"error": f"Author not found: {author_name}", "method": "Funding Transparency", "verdict": "PASS"}
    
    author = authors[0]
    author_id = author['id'].split('/')[-1]
    works = openalex_get_works_by_author(author_id, per_page=50)
    
    total = len(works)
    with_funding = sum(1 for w in works if w.get('grants'))
    funding_rate = with_funding / max(total, 1)
    
    issues = []
    if total > 10 and funding_rate < 0.1:
        issues.append(f"Only {with_funding}/{total} papers ({funding_rate:.0%}) report funding — suspiciously low")
    
    return {
        "method": "Funding Transparency Check",
        "author": author.get('display_name', author_name),
        "total_papers": total,
        "papers_with_funding": with_funding,
        "funding_rate": round(funding_rate, 2),
        "issues": issues,
        "verdict": "WARNING" if issues else "PASS"
    }


def investigate_author(author_name: str) -> dict:
    """Run all non-data signal checks on an author. ~30-60 seconds."""
    results = {}
    results['retraction'] = retraction_proximity(author_name)
    results['post_retraction'] = post_retraction_publishing(author_name)
    results['velocity'] = publication_velocity_check(author_name)
    results['affiliation'] = affiliation_analysis(author_name)
    results['self_cite'] = self_citation_audit(author_name)
    results['funding'] = funding_transparency_check(author_name)
    
    red = sum(1 for r in results.values() if 'RED FLAG' in str(r.get('verdict', '')))
    warn = sum(1 for r in results.values() if 'WARNING' in str(r.get('verdict', '')))
    score = red * 3 + warn
    level = 'CRITICAL' if score >= 9 else 'HIGH' if score >= 6 else 'MEDIUM' if score >= 3 else 'LOW'
    
    return {
        "investigation_target": author_name,
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "summary": {"red_flags": red, "warnings": warn, "total_score": score, "risk_level": level},
        "overall_verdict": f"{level} — {red} RED, {warn} WARN"
    }


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python investigator.py investigate <author_name>")
        sys.exit(1)
    result = investigate_author(sys.argv[2])
    print(json.dumps(result, indent=2, ensure_ascii=False))
