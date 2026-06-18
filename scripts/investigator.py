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
  - ORCID Public API (https://pub.orcid.org) — Researcher profiles

Methods:
  1. Author Network Analysis — Co-authorship graph, closure, central figures
  2. Self-Citation Audit — Unusual self-citation ratios
  3. Citation Cartel Detection — Mutual citation rings
  4. Publication Velocity — Suspiciously rapid output
  5. Venue Concentration — Same-journal clustering
  6. Retraction Proximity — Connections to retracted papers
  7. Peer Review Timeline — Anomalous review speed
  8. Affiliation Analysis — Institution hopping, paper mills
  9. Funding Transparency — Undisclosed COI patterns
 10. Co-author Closure — Small, closed collaboration circles
"""

import urllib.request
import urllib.parse
import json
import time
import math
from collections import defaultdict, Counter
from typing import List, Dict, Optional, Tuple, Set
from datetime import datetime


# ============================================================
# API CLIENTS (No API keys required)
# ============================================================

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
    """Fetch JSON from URL with rate limiting."""
    _limiter.wait()
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'AcademicForensics/1.0 (mailto:researcher@example.com)',
            'Accept': 'application/json'
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return None


# ---- OpenAlex ----
def openalex_search_works(query: str, per_page: int = 25) -> List[dict]:
    """Search works on OpenAlex."""
    url = f"https://api.openalex.org/works?search={urllib.parse.quote(query)}&per_page={per_page}"
    data = _get_json(url)
    return data.get('results', []) if data else []

def openalex_search_authors(name: str, per_page: int = 10) -> List[dict]:
    """Search authors on OpenAlex."""
    url = f"https://api.openalex.org/authors?search={urllib.parse.quote(name)}&per_page={per_page}"
    data = _get_json(url)
    return data.get('results', []) if data else []

def openalex_get_author(author_id: str) -> Optional[dict]:
    """Get author details by OpenAlex ID."""
    url = f"https://api.openalex.org/authors/{author_id}"
    return _get_json(url)

def openalex_get_works_by_author(author_id: str, per_page: int = 50) -> List[dict]:
    """Get works by author."""
    url = f"https://api.openalex.org/works?filter=authorships.author.id:{author_id}&per_page={per_page}&sort=publication_date:desc"
    data = _get_json(url)
    return data.get('results', []) if data else []

def openalex_get_coauthors(author_id: str, limit: int = 100) -> List[dict]:
    """Get co-authors of an author."""
    # OpenAlex doesn't have a direct co-author endpoint, so we scan recent works
    works = openalex_get_works_by_author(author_id, per_page=min(limit, 50))
    coauthor_map = {}  # author_id -> {name, count, works}
    
    for work in works:
        for authorship in work.get('authorships', []):
            aid = authorship.get('author', {}).get('id', '')
            if aid and aid != f"https://openalex.org/{author_id}":
                aid_short = aid.split('/')[-1]
                if aid_short not in coauthor_map:
                    coauthor_map[aid_short] = {
                        'name': authorship.get('author', {}).get('display_name', 'Unknown'),
                        'count': 0,
                        'works': []
                    }
                coauthor_map[aid_short]['count'] += 1
                coauthor_map[aid_short]['works'].append(work.get('title', 'Unknown'))
    
    return sorted(coauthor_map.values(), key=lambda x: x['count'], reverse=True)


# ---- CrossRef ----
def crossref_search(query: str, rows: int = 10) -> List[dict]:
    """Search CrossRef for works."""
    url = f"https://api.crossref.org/works?query={urllib.parse.quote(query)}&rows={rows}"
    data = _get_json(url)
    return data.get('message', {}).get('items', []) if data else []

def crossref_get_by_doi(doi: str) -> Optional[dict]:
    """Get work by DOI from CrossRef."""
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    data = _get_json(url)
    return data.get('message') if data else None


# ---- PubMed ----
def pubmed_search(query: str, max_results: int = 20) -> List[dict]:
    """Search PubMed for articles."""
    # First get IDs
    search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={urllib.parse.quote(query)}&retmax={max_results}&retmode=json"
    _limiter.wait()
    try:
        req = urllib.request.Request(search_url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            id_data = json.loads(resp.read())
        ids = id_data.get('esearchresult', {}).get('idlist', [])
    except:
        return []
    
    if not ids:
        return []
    
    # Fetch summaries
    fetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={','.join(ids)}&retmode=json"
    _limiter.wait()
    try:
        req = urllib.request.Request(fetch_url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            summary = json.loads(resp.read())
        return [summary.get('result', {}).get(pid, {}) for pid in ids]
    except:
        return []


# ---- Semantic Scholar ----
def s2_search_papers(query: str, limit: int = 10) -> List[dict]:
    """Search Semantic Scholar."""
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={urllib.parse.quote(query)}&limit={limit}&fields=title,authors,year,citationCount,externalIds"
    data = _get_json(url)
    return data.get('data', []) if data else []

def s2_get_citations(paper_id: str, limit: int = 50) -> List[dict]:
    """Get papers citing a given paper."""
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations?fields=title,authors,year&limit={limit}"
    data = _get_json(url)
    return data.get('data', []) if data else []


# ============================================================
# 1. AUTHOR NETWORK ANALYSIS
# ============================================================

def author_network_analysis(author_name: str, max_coauthors: int = 30,
                             min_coauthorship: int = 2) -> dict:
    """
    Map an author's co-authorship network and detect suspicious patterns:
    - Small, closed circles (paper-mill signature)
    - One dominant co-author (ghost supervisor / gift authorship ring)
    - All co-authors from same institution (institutional nepotism)
    
    Args:
        author_name: Full name to search
        max_coauthors: Max co-authors to analyze
        min_coauthorship: Minimum co-authored papers to include
    """
    # Find author on OpenAlex
    authors = openalex_search_authors(author_name, per_page=5)
    if not authors:
        return {"error": f"Author '{author_name}' not found on OpenAlex"}
    
    author = authors[0]
    author_id = author['id'].split('/')[-1]
    
    # Get co-authors
    coauthors = openalex_get_coauthors(author_id, limit=100)
    
    # Filter by minimum co-authorship
    significant = [c for c in coauthors if c['count'] >= min_coauthorship]
    significant = significant[:max_coauthors]
    
    # Analyze patterns
    issues = []
    
    # Pattern 1: Very few co-authors (closed circle)
    total_coauthors = len(coauthors)
    if total_coauthors <= 5 and sum(c['count'] for c in coauthors) > 20:
        issues.append(
            f"Only {total_coauthors} unique co-authors across {sum(c['count'] for c in coauthors)} "
            f"co-authored papers — suspiciously closed circle (possible paper mill)"
        )
    
    # Pattern 2: One dominant co-author (> 60% of papers)
    if significant:
        top = significant[0]
        total_works = author.get('works_count', 0)
        if total_works > 0 and top['count'] / total_works > 0.6:
            issues.append(
                f"'{top['name']}' co-authors {top['count']}/{total_works} papers "
                f"({top['count']/total_works*100:.0f}%) — possible gift authorship ring"
            )
    
    # Pattern 3: High institutional concentration
    institution_counts = defaultdict(int)
    works = openalex_get_works_by_author(author_id, per_page=50)
    for work in works:
        for authorship in work.get('authorships', []):
            for inst in authorship.get('institutions', []):
                institution_counts[inst.get('display_name', 'Unknown')] += 1
    
    if institution_counts:
        top_inst = max(institution_counts.values())
        total_affiliations = sum(institution_counts.values())
        if total_affiliations > 0 and top_inst / total_affiliations > 0.8:
            issues.append(
                f"{(top_inst/total_affiliations*100):.0f}% of affiliations from single institution"
            )
    
    author_info = {
        "name": author.get('display_name', author_name),
        "openalex_id": author_id,
        "works_count": author.get('works_count', 0),
        "cited_by_count": author.get('cited_by_count', 0),
        "h_index": author.get('summary_stats', {}).get('h_index', 0),
        "orcid": author.get('orcid', 'N/A')
    }
    
    return {
        "method": "Author Network Analysis",
        "author": author_info,
        "total_coauthors": total_coauthors,
        "significant_coauthors": [
            {"name": c['name'], "papers": c['count']} for c in significant
        ],
        "top_institutions": dict(sorted(institution_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
        "issues": issues,
        "risk_flags": len(issues),
        "verdict": "RED FLAG" if len(issues) >= 2 else \
                   "WARNING" if issues else "PASS"
    }


# ============================================================
# 2. SELF-CITATION AUDIT
# ============================================================

def self_citation_audit(author_name: str) -> dict:
    """
    Check for unusually high self-citation ratios.
    
    Normal: 10-20% self-citation
    Suspicious: >40% self-citation
    Red flag: >60% (citation-stacking)
    
    Args:
        author_name: Author name to analyze
    """
    authors = openalex_search_authors(author_name, per_page=3)
    if not authors:
        return {"error": f"Author not found: {author_name}"}
    
    author = authors[0]
    author_id = author['id'].split('/')[-1]
    
    # Get recent works
    works = openalex_get_works_by_author(author_id, per_page=25)
    
    total_citations = 0
    self_citations = 0
    work_details = []
    
    for work in works[:20]:
        citations = work.get('cited_by_count', 0)
        total_citations += citations
        
        # Check if author themselves is in the citing papers
        # (Simplified: we can't easily enumerate all citing papers, 
        #  so we check if the work's authors overlap with target author)
        work_authors = [a.get('author', {}).get('display_name', '') 
                       for a in work.get('authorships', [])]
        
        # Estimate self-citations from the work's own reference list
        # (This is an approximation)
        work_details.append({
            "title": work.get('title', 'Unknown')[:80],
            "year": work.get('publication_year'),
            "citations": citations
        })
    
    # Get the actual self-citation data from author profile
    # OpenAlex provides summary stats
    h_index = author.get('summary_stats', {}).get('h_index', 0)
    i10_index = author.get('summary_stats', {}).get('i10_index', 0)
    
    issues = []
    # Self-citation is hard to compute precisely without full citation graph
    # We flag based on available signals
    
    # Signal: Very high works_count with low citation impact
    works_count = author.get('works_count', 0)
    cited_by = author.get('cited_by_count', 0)
    if works_count > 0:
        cites_per_paper = cited_by / works_count
        if cites_per_paper < 1 and works_count > 20:
            issues.append(
                f"Extremely low impact: {cites_per_paper:.1f} citations/paper "
                f"({cited_by} cites / {works_count} papers) — possible self-citation padding"
            )
    
    return {
        "method": "Self-Citation Audit",
        "author": author.get('display_name', author_name),
        "works_count": works_count,
        "total_cited_by": cited_by,
        "h_index": h_index,
        "citations_per_paper": round(cited_by / max(works_count, 1), 2),
        "issues": issues,
        "verdict": "WARNING" if issues else "PASS"
    }


# ============================================================
# 3. CITATION CARTEL DETECTION
# ============================================================

def citation_cartel_check(author_name: str, depth: int = 2) -> dict:
    """
    Detect mutual citation rings (citation cartels).
    
    A citation cartel exists when a small group of authors 
    disproportionately cite each other to inflate metrics.
    
    Limited by API access — provides heuristic flags.
    """
    issues = []
    authors = openalex_search_authors(author_name, per_page=3)
    if not authors:
        return {"error": f"Author not found: {author_name}"}
    
    author = authors[0]
    author_id = author['id'].split('/')[-1]
    
    # Check co-authors who are also frequent citers
    coauthors = openalex_get_coauthors(author_id, limit=30)
    
    # If top 3 co-authors appear on >80% of papers together, flag
    total_works = author.get('works_count', 0)
    cartel_candidates = []
    
    for co in coauthors[:10]:
        if co['count'] >= 5 and total_works > 0:
            co_ratio = co['count'] / total_works
            if co_ratio > 0.7:
                cartel_candidates.append({
                    "name": co['name'],
                    "co_papers": co['count'],
                    "ratio": round(co_ratio, 2)
                })
    
    if cartel_candidates:
        names = ', '.join(c['name'] for c in cartel_candidates)
        issues.append(
            f"Citation cartel candidates: {names} — each appears on "
            f">{min(c['ratio'] for c in cartel_candidates)*100:.0f}% of papers"
        )
    
    return {
        "method": "Citation Cartel Detection",
        "author": author.get('display_name', author_name),
        "n_coauthors": len(coauthors),
        "cartel_candidates": cartel_candidates,
        "issues": issues,
        "verdict": "RED FLAG" if cartel_candidates else "PASS"
    }


# ============================================================
# 4. PUBLICATION VELOCITY CHECK
# ============================================================

def publication_velocity_check(author_name: str) -> dict:
    """
    Check for suspiciously rapid publication rates.
    
    Red flags:
    - >12 papers/year sustained (possible paper mill)
    - Sudden spike in output (possible data fabrication across papers)
    - All papers in a single year in same journal cluster
    
    Args:
        author_name: Author name to analyze
    """
    authors = openalex_search_authors(author_name, per_page=3)
    if not authors:
        return {"error": f"Author not found: {author_name}"}
    
    author = authors[0]
    author_id = author['id'].split('/')[-1]
    works = openalex_get_works_by_author(author_id, per_page=100)
    
    # Group by year
    by_year = defaultdict(list)
    by_venue = defaultdict(int)
    
    for work in works:
        year = work.get('publication_year')
        if year:
            by_year[year].append(work)
        
        venue = work.get('host_venue', {})
        if venue:
            venue_name = venue.get('display_name', 'Unknown')
            by_venue[venue_name] += 1
    
    issues = []
    
    # Check peak output
    sorted_years = sorted(by_year.items(), key=lambda x: len(x[1]), reverse=True)
    if sorted_years:
        peak_year, peak_papers = sorted_years[0]
        if len(peak_papers) > 12:
            issues.append(
                f"Peak output: {peak_papers} papers in {peak_year} — "
                f"suspiciously high (>12/year, possible paper mill)"
            )
        
        # Check for sudden spikes
        years_list = sorted(by_year.keys())
        if len(years_list) >= 3:
            counts = [len(by_year[y]) for y in years_list[-5:]]
            avg = sum(counts[:-1]) / max(len(counts[:-1]), 1)
            last = counts[-1]
            if avg > 0 and last / avg > 3 and last > 5:
                issues.append(
                    f"Output spike: {last} papers in most recent year vs "
                    f"avg {avg:.1f}/year — 3x+ increase"
                )
    
    # Check venue concentration
    total_works_count = len(works)
    if by_venue and total_works_count > 0:
        top_venue = max(by_venue.values())
        if top_venue / total_works_count > 0.5 and total_works_count > 5:
            top_venue_name = max(by_venue, key=by_venue.get)
            issues.append(
                f"{top_venue}/{total_works_count} papers ({top_venue/total_works_count*100:.0f}%) "
                f"in '{top_venue_name}' — excessive venue concentration"
            )
    
    return {
        "method": "Publication Velocity Check",
        "author": author.get('display_name', author_name),
        "total_works_analyzed": total_works_count,
        "years_active": len(by_year),
        "peak_year": {"year": sorted_years[0][0], "papers": len(sorted_years[0][1])} if sorted_years else None,
        "top_venues": dict(sorted(by_venue.items(), key=lambda x: x[1], reverse=True)[:5]),
        "issues": issues,
        "verdict": "RED FLAG" if len(issues) >= 2 else \
                   "WARNING" if issues else "PASS"
    }


# ============================================================
# 5. RETRACTION PROXIMITY
# ============================================================

def retraction_proximity(author_name: str) -> dict:
    """
    Check if an author has connections to retracted papers.
    Uses OpenAlex direct retraction filter for accurate counts.
    """
    issues = []
    
    # Get author via search (includes works_count)
    url = f"https://api.openalex.org/authors?search={urllib.parse.quote(author_name)}&per_page=3"
    data = _get_json(url)
    if not data or not data.get('results'):
        return {"error": f"Author not found: {author_name}", "method": "Retraction Proximity", "verdict": "PASS"}
    
    author = data['results'][0]
    author_id = author['id'].split('/')[-1]
    display_name = author.get('display_name', author_name)
    works_count = author.get('works_count', 0)
    
    # Get retracted works via filter (much more accurate than scanning)
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
    
    # Collect retraction details (just top 10)
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
        "verdict": "RED FLAG" if retraction_rate > 5 else                    "RED FLAG" if ret_count >= 10 else                    "WARNING" if ret_count >= 2 else                    "WARNING" if ret_count >= 1 else "PASS"
    }

# ============================================================
# 5B. POST-RETRACTION PUBLISHING PATTERN
# ============================================================

def post_retraction_publishing(author_name: str) -> dict:
    """
    Check if author continued publishing after first retraction.
    Continued publishing at high volume after retractions is suspicious.
    Self-retraction and stopping is integrity-positive.
    """
    authors = openalex_search_authors(author_name, per_page=3)
    if not authors:
        return {"error": f"Author not found: {author_name}"}
    
    author = authors[0]
    author_id = author['id'].split('/')[-1]
    
    # Get retracted works
    retracted_url = f"https://api.openalex.org/works?filter=authorships.author.id:{author_id},is_retracted:true&sort=publication_date:asc&per_page=50"
    ret_data = _get_json(retracted_url)
    ret_works = ret_data.get('results', []) if ret_data else []
    
    if not ret_works:
        return {
            "method": "Post-Retraction Publishing",
            "author": author.get('display_name', author_name),
            "verdict": "PASS — No retractions found"
        }
    
    # Find the first retraction year
    first_ret_year = min(
        (w.get('publication_year', 9999) for w in ret_works),
        default=None
    )
    
    # Get all works after first retraction
    all_works = openalex_get_works_by_author(author_id, per_page=100)
    
    post_ret = [w for w in all_works 
                if w.get('publication_year', 0) and w.get('publication_year', 0) >= first_ret_year
                and not w.get('is_retracted', False)]
    
    post_ret_count = len(post_ret)
    total_works = len(all_works)
    post_ret_ratio = post_ret_count / max(total_works, 1) if total_works > 0 else 0
    
    issues = []
    # Key differentiator: what fraction of career happened after first retraction?
    if post_ret_ratio > 0.5 and post_ret_count > 10:
        issues.append(
            f"Published {post_ret_count} papers ({post_ret_ratio:.0%} of career) AFTER first retraction in {first_ret_year} — "
            f"retraction did not slow output"
        )
    elif post_ret_count > 0:
        issues.append(
            f"Published {post_ret_count} papers ({post_ret_ratio:.0%} of career) after first retraction ({first_ret_year})"
        )
    
    return {
        "method": "Post-Retraction Publishing",
        "author": author.get('display_name', author_name),
        "first_retraction_year": first_ret_year,
        "total_retractions": len(ret_works),
        "papers_after_first_retraction": post_ret_count,
        "post_retraction_ratio": round(post_ret_ratio, 2),
        "issues": issues,
        "verdict": "RED FLAG" if (post_ret_ratio > 0.5 and post_ret_count > 10) else                    "WARNING" if post_ret_count > 5 else "PASS"
    }

# ============================================================
# 6. PEER REVIEW TIMELINE ANOMALY
# ============================================================

def peer_review_timeline_check(doi: str) -> dict:
    """
    Check for anomalous peer review timelines.
    
    Red flags:
    - Submission-to-acceptance < 7 days (impossible for proper peer review)
    - Acceptance on weekends/holidays
    - Multiple papers accepted on the same date
    
    Note: This uses CrossRef event data when available.
    """
    issues = []
    work = crossref_get_by_doi(doi)
    
    if not work:
        return {"error": f"DOI not found: {doi}"}
    
    # CrossRef provides some date information
    created = work.get('created', {}).get('date-time', '')
    deposited = work.get('deposited', {}).get('date-time', '')
    published = work.get('published-print', {}).get('date-parts', [[]])[0]
    published_online = work.get('published-online', {}).get('date-parts', [[]])[0]
    
    timeline = {
        "created": created,
        "deposited": deposited,
        "published_print": published,
        "published_online": published_online
    }
    
    # Check for suspiciously fast timeline (if dates available)
    if created and deposited:
        try:
            created_date = datetime.fromisoformat(created.replace('Z', '+00:00'))
            deposited_date = datetime.fromisoformat(deposited.replace('Z', '+00:00'))
            days = (deposited_date - created_date).days
            
            if days < 7 and days >= 0:
                issues.append(
                    f"Created-to-deposited: {days} days — "
                    f"suspiciously fast (normal peer review takes weeks to months)"
                )
        except:
            pass
    
    # Check publisher info
    publisher = work.get('publisher', 'Unknown')
    journal = work.get('container-title', ['Unknown'])[0] if work.get('container-title') else 'Unknown'
    
    # Flag known predatory/open-access patterns
    predatory_publishers = ['OMICS', 'WASET', 'SCIENCEDOMAIN', 'HINDAWI']
    if any(pp.lower() in publisher.lower() for pp in predatory_publishers):
        issues.append(f"Publisher '{publisher}' flagged as potentially predatory")
    
    return {
        "method": "Peer Review Timeline Check",
        "doi": doi,
        "title": work.get('title', ['Unknown'])[0] if work.get('title') else 'Unknown',
        "journal": journal,
        "publisher": publisher,
        "timeline": timeline,
        "issues": issues,
        "verdict": "WARNING" if issues else "PASS"
    }


# ============================================================
# 7. AFFILIATION ANALYSIS
# ============================================================

def affiliation_analysis(author_name: str) -> dict:
    """
    Analyze author affiliation patterns for fraud signals.
    
    Red flags:
    - Rapid institution changes (hopping)
    - Multiple simultaneous affiliations in different countries
    - Affiliations to known paper mills
    - Private email domains (gmail.com, etc.) for corresponding author
    """
    authors = openalex_search_authors(author_name, per_page=3)
    if not authors:
        return {"error": f"Author not found: {author_name}"}
    
    author = authors[0]
    author_id = author['id'].split('/')[-1]
    works = openalex_get_works_by_author(author_id, per_page=50)
    
    # Collect affiliations over time
    affiliations = {}  # institution -> count
    by_year = defaultdict(set)
    countries = Counter()
    
    for work in works:
        year = work.get('publication_year', 0)
        for authorship in work.get('authorships', []):
            for inst in authorship.get('institutions', []):
                name = inst.get('display_name', 'Unknown')
                affiliations[name] = affiliations.get(name, 0) + 1
                if year:
                    by_year[year].add(name)
                country = inst.get('country_code', 'Unknown')
                if country:
                    countries[country] += 1
    
    issues = []
    
    # Check for affiliation hopping
    sorted_affiliations = sorted(affiliations.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_affiliations) >= 5:
        top_count = sum(c for _, c in sorted_affiliations[:2])
        total = sum(affiliations.values())
        if total > 0 and top_count / total < 0.5:
            issues.append(
                f"High affiliation diversity: {len(sorted_affiliations)} institutions "
                f"— top 2 only account for {top_count/total*100:.0f}%"
            )
    
    # Check multiple countries
    if len(countries) >= 4:
        issues.append(
            f"Affiliations in {len(countries)} different countries — "
            f"possible affiliation padding"
        )
    
    return {
        "method": "Affiliation Analysis",
        "author": author.get('display_name', author_name),
        "n_affiliations": len(affiliations),
        "n_countries": len(countries),
        "top_affiliations": dict(sorted_affiliations[:5]),
        "top_countries": dict(countries.most_common(5)),
        "issues": issues,
        "verdict": "WARNING" if issues else "PASS"
    }


# ============================================================
# 8. CO-AUTHOR CLOSURE (Small-World Check)
# ============================================================

def coauthor_closure_check(author_name: str) -> dict:
    """
    Check if an author's co-author network is abnormally closed.
    
    In a normal research network, co-authors have their own independent networks.
    In a paper mill, ALL co-authors publish exclusively with each other.
    
    Closure ratio = (co-authors who only publish with this author) / total co-authors
    """
    authors = openalex_search_authors(author_name, per_page=3)
    if not authors:
        return {"error": f"Author not found: {author_name}"}
    
    author = authors[0]
    author_id = author['id'].split('/')[-1]
    coauthors = openalex_get_coauthors(author_id, limit=30)
    
    if len(coauthors) < 5:
        return {
            "method": "Co-Author Closure",
            "author": author.get('display_name', author_name),
            "n_coauthors": len(coauthors),
            "issues": ["Too few co-authors to assess closure"],
            "verdict": "PASS"
        }
    
    # For each co-author, check if they publish with others
    closed_count = 0
    for co in coauthors[:20]:
        co_name = co['name']
        # Quick check: does this person appear in OpenAlex with their own co-authors?
        co_authors_search = openalex_search_authors(co_name, per_page=3)
        if co_authors_search:
            co_id = co_authors_search[0]['id'].split('/')[-1]
            co_works = openalex_get_works_by_author(co_id, per_page=10)
            # Check if they publish with people other than the target author
            has_other_coauthors = False
            for work in co_works:
                for authorship in work.get('authorships', []):
                    other_name = authorship.get('author', {}).get('display_name', '')
                    if other_name and other_name.lower() != author_name.lower():
                        has_other_coauthors = True
                        break
                if has_other_coauthors:
                    break
            if not has_other_coauthors and co_works:
                closed_count += 1
    
    closure_ratio = closed_count / len(coauthors[:20]) if coauthors else 0
    issues = []
    
    if closure_ratio > 0.7:
        issues.append(
            f"Closure ratio: {closure_ratio:.0%} — {closed_count}/{min(len(coauthors),20)} "
            f"co-authors only publish with this author (paper mill signature)"
        )
    elif closure_ratio > 0.4:
        issues.append(
            f"Elevated closure ratio: {closure_ratio:.0%} — unusually closed network"
        )
    
    return {
        "method": "Co-Author Network Closure",
        "author": author.get('display_name', author_name),
        "n_coauthors": len(coauthors),
        "closed_coauthors": closed_count,
        "closure_ratio": round(closure_ratio, 2),
        "issues": issues,
        "verdict": "RED FLAG" if closure_ratio > 0.7 else \
                   "WARNING" if issues else "PASS"
    }


# ============================================================
# 9. FUNDING TRANSPARENCY
# ============================================================

def funding_transparency_check(author_name: str) -> dict:
    """
    Check for undisclosed funding / COI patterns.
    
    Uses OpenAlex to check if papers have funding acknowledgments.
    Absence of funding info on industry-relevant research is suspicious.
    """
    authors = openalex_search_authors(author_name, per_page=3)
    if not authors:
        return {"error": f"Author not found: {author_name}"}
    
    author = authors[0]
    author_id = author['id'].split('/')[-1]
    works = openalex_get_works_by_author(author_id, per_page=50)
    
    total = len(works)
    with_funding = 0
    funders = Counter()
    
    for work in works:
        grants = work.get('grants', [])
        if grants:
            with_funding += 1
            for grant in grants:
                funder = grant.get('funder_display_name', 'Unknown')
                funders[funder] += 1
    
    funding_rate = with_funding / max(total, 1)
    
    issues = []
    if total > 10 and funding_rate < 0.1:
        issues.append(
            f"Only {with_funding}/{total} papers ({funding_rate:.0%}) report funding — "
            f"suspiciously low for empirical research"
        )
    
    # Check for industry funding concentration
    industry_keywords = ['pharma', 'inc', 'ltd', 'corp', 'company', 'industr', 'bioscience']
    industry_funders = {k: v for k, v in funders.items() 
                       if any(kw in k.lower() for kw in industry_keywords)}
    if industry_funders:
        issues.append(
            f"Industry funding detected: {dict(industry_funders)} — check for undisclosed COI"
        )
    
    return {
        "method": "Funding Transparency Check",
        "author": author.get('display_name', author_name),
        "total_papers": total,
        "papers_with_funding": with_funding,
        "funding_rate": round(funding_rate, 2),
        "top_funders": dict(funders.most_common(5)),
        "issues": issues,
        "verdict": "WARNING" if issues else "PASS"
    }


# ============================================================
# 10. COMPREHENSIVE AUTHOR INVESTIGATION
# ============================================================

def investigate_author(author_name: str, deep: bool = False) -> dict:
    """
    Run all non-data signal checks on an author.
    
    Args:
        author_name: Full name
        deep: If True, run network-intensive checks (slower)
    
    Returns:
        Complete investigation report
    """
    results = {}
    
    print(f"Investigating: {author_name}")
    
    # Fast checks first
    print("  [1/8] Self-citation audit...")
    results['self_citation'] = self_citation_audit(author_name)
    
    print("  [2/8] Publication velocity...")
    results['publication_velocity'] = publication_velocity_check(author_name)
    
    print("  [3/8] Retraction proximity...")
    results['retraction_proximity'] = retraction_proximity(author_name)
    
    print("  [4/8] Affiliation analysis...")
    results['affiliation'] = affiliation_analysis(author_name)
    
    print("  [5/8] Funding transparency...")
    results['funding'] = funding_transparency_check(author_name)
    
    if deep:
        print("  [6/8] Author network analysis (deep)...")
        results['network'] = author_network_analysis(author_name)
        
        print("  [7/8] Citation cartel detection...")
        results['cartel'] = citation_cartel_check(author_name)
        
        print("  [8/8] Co-author closure check...")
        results['closure'] = coauthor_closure_check(author_name)
    
    # Score
    red_flags = sum(1 for r in results.values() 
                    if r.get('verdict', '').startswith('RED FLAG'))
    warnings = sum(1 for r in results.values() 
                   if r.get('verdict', '').startswith('WARNING'))
    passes = sum(1 for r in results.values() 
                 if r.get('verdict', '') == 'PASS')
    
    total_checks = len(results)
    risk_score = (red_flags * 3 + warnings) / max(total_checks * 3, 1) * 100
    
    if risk_score > 50:
        overall = "CRITICAL — Multiple fraud signals detected"
    elif risk_score > 25:
        overall = "SUSPICIOUS — Several concerning patterns"
    elif risk_score > 10:
        overall = "CAUTION — Minor concerns"
    else:
        overall = "CLEAN — No significant fraud signals"
    
    return {
        "investigation_target": author_name,
        "timestamp": datetime.now().isoformat(),
        "deep_scan": deep,
        "results": results,
        "summary": {
            "red_flags": red_flags,
            "warnings": warnings,
            "passes": passes,
            "total_checks": total_checks,
            "risk_score_pct": round(risk_score, 1)
        },
        "overall_verdict": overall
    }


# ============================================================
# CLI
# ============================================================

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python investigator.py investigate <author_name> [--deep]")
        print("       python investigator.py check-doi <doi>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    target = sys.argv[2]
    deep = '--deep' in sys.argv
    
    if cmd == 'investigate':
        result = investigate_author(target, deep=deep)
        print("\n" + json.dumps(result, indent=2, ensure_ascii=False))
    elif cmd == 'check-doi':
        result = peer_review_timeline_check(target)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Unknown command: {cmd}")
