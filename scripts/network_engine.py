#!/usr/bin/env python3
"""
TruthTracer Network Engine — Author Investigation via Open APIs
Uses: OpenAlex, CrossRef, PubMed (no API keys required)
"""

import urllib.request, urllib.parse, json, time
from collections import defaultdict, Counter

_limiter_last = 0
def _rate_limit(calls_per_sec=10):
    global _limiter_last
    elapsed = time.time() - _limiter_last
    if elapsed < 1.0/calls_per_sec: time.sleep(1.0/calls_per_sec - elapsed)
    _limiter_last = time.time()

def _get_json(url, timeout=15):
    _rate_limit()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'TruthTracer/2.2', 'Accept': 'application/json'})
        return json.loads(urllib.request.urlopen(req, timeout=timeout).read())
    except: return None

# ── Core functions ──

def search_author(name: str) -> dict:
    """Search OpenAlex for an author."""
    data = _get_json(f"https://api.openalex.org/authors?search={urllib.parse.quote(name)}&per_page=3")
    return data.get('results', [])[0] if data and data.get('results') else None

def get_retractions(author_id: str) -> tuple:
    """Get retraction count and works_count for an author."""
    ret_url = f"https://api.openalex.org/works?filter=authorships.author.id:{author_id},is_retracted:true&per_page=200"
    ret_data = _get_json(ret_url)
    ret_count = ret_data.get('meta', {}).get('count', 0) if ret_data else 0
    return ret_count

def investigate_author(name: str, deep: bool = False) -> dict:
    """Full investigation of a single author."""
    author = search_author(name)
    if not author: return {"name": name, "found": False}
    
    aid = author['id'].split('/')[-1]
    works = author.get('works_count', 0)
    cited = author.get('cited_by_count', 0)
    h = author.get('summary_stats', {}).get('h_index', 0)
    ret_count = get_retractions(aid)
    rate = ret_count / max(works, 1) * 100
    
    risk = "RED FLAG" if rate > 10 or ret_count >= 10 else \
           "WARNING" if rate > 2 or ret_count >= 3 else \
           "WARNING" if ret_count >= 1 else "PASS"
    
    result = {"name": author.get('display_name', name), "found": True,
              "works": works, "cited": cited, "h_index": h,
              "retractions": ret_count, "rate_pct": round(rate, 2),
              "verdict": risk}
    
    if deep:
        # Get velocity
        wdata = _get_json(f"https://api.openalex.org/works?filter=authorships.author.id:{aid}&per_page=100&sort=publication_date:desc")
        by_year = defaultdict(int)
        if wdata:
            for w in wdata.get('results', []):
                y = w.get('publication_year', 0)
                if y: by_year[y] += 1
        peak = max(by_year.values()) if by_year else 0
        peak_year = max(by_year, key=by_year.get) if by_year else None
        result['peak_output'] = {'year': peak_year, 'count': peak}
        if peak > 15: result['velocity_flag'] = "WARNING"
    
    return result

def investigate_paper_authors(author_ids: list) -> dict:
    """Investigate all authors of a paper."""
    results = {}
    total_ret = 0
    for aid in author_ids:
        name = aid.split('/')[-1] if '/' in aid else aid
        ret_count = get_retractions(aid)
        total_ret += ret_count
        results[name] = ret_count
    red = sum(1 for r in results.values() if r >= 10)
    risk = "RED FLAG" if total_ret >= 50 else "WARNING" if total_ret >= 10 else "PASS"
    return {"authors": results, "total_retractions": total_ret, "red_flag_authors": red, "verdict": risk}

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3: print("Usage: network_engine.py investigate <name>"); sys.exit(1)
    result = investigate_author(sys.argv[2], deep='--deep' in sys.argv)
    print(json.dumps(result, indent=2, ensure_ascii=False))
