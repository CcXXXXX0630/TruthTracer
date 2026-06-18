#!/usr/bin/env python3
"""
Case Builder — Evidence Assembly, Scoring, and Reporting
=========================================================
Combines statistical forensics + investigator signals into a unified
risk assessment with professional audit report generation.

Scoring System:
  Each RED FLAG = 3 points
  Each WARNING  = 1 point
  
  Risk Level:
    0-5    = LOW — No significant evidence of fabrication
    6-12   = MEDIUM — Several concerning patterns, closer scrutiny
    13-20  = HIGH — Strong evidence, escalate to editor
    21+    = CRITICAL — Overwhelming evidence, retraction review
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


def score_evidence(forensics_result: dict, investigation_result: dict = None) -> dict:
    """Combine statistical and non-data signals into a unified risk score."""
    evidence_items = []
    total_score = 0
    red_flags = 0
    warnings = 0
    
    # Score statistical evidence
    if forensics_result:
        for method, result in forensics_result.get('results', {}).items():
            if isinstance(result, list):
                for item in result:
                    verdict = item.get('verdict', '')
                    evidence_items.append({
                        'source': 'statistical', 'method': method,
                        'verdict': verdict,
                        'detail': item.get('message', str(item.get('issues', ''))[:200])
                    })
                    if 'RED FLAG' in verdict:
                        total_score += 3; red_flags += 1
                    elif 'WARNING' in verdict:
                        total_score += 1; warnings += 1
            elif isinstance(result, dict):
                verdict = result.get('verdict', '')
                evidence_items.append({
                    'source': 'statistical', 'method': method,
                    'verdict': verdict,
                    'detail': result.get('message', str(result.get('issues', ''))[:200])
                })
                if 'RED FLAG' in verdict:
                    total_score += 3; red_flags += 1
                elif 'WARNING' in verdict:
                    total_score += 1; warnings += 1
    
    # Score investigator evidence
    if investigation_result:
        for method, result in investigation_result.get('results', {}).items():
            verdict = result.get('verdict', '')
            evidence_items.append({
                'source': 'investigator', 'method': method,
                'verdict': verdict,
                'detail': str(result.get('issues', ''))[:200]
            })
            if 'RED FLAG' in verdict:
                total_score += 3; red_flags += 1
            elif 'WARNING' in verdict:
                total_score += 1; warnings += 1
    
    if total_score <= 5:
        risk, recommendation = "LOW", "No significant evidence of fabrication. Standard review may proceed."
    elif total_score <= 12:
        risk, recommendation = "MEDIUM", "Several concerning patterns. Recommend closer scrutiny and verification of key data points."
    elif total_score <= 20:
        risk, recommendation = "HIGH", "Strong evidence of irregularities. Recommend escalation to journal editor / institution."
    else:
        risk, recommendation = "CRITICAL", "Overwhelming evidence of fabrication. Recommend immediate retraction review."
    
    return {
        "total_score": total_score, "red_flags": red_flags, "warnings": warnings,
        "risk_level": risk, "recommendation": recommendation, "evidence_items": evidence_items
    }


def generate_report(forensics_result: dict = None, investigation_result: dict = None,
                    paper_title: str = "Untitled Investigation", output_path: str = None) -> str:
    """Generate a professional investigation report in Markdown."""
    scored = score_evidence(forensics_result, investigation_result)
    
    lines = []
    lines.append(f"# Academic Integrity Investigation Report")
    lines.append(f"**Target**: {paper_title}")
    lines.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Classification**: CONFIDENTIAL")
    lines.append(f"")
    
    risk = scored['risk_level']
    emoji = {'LOW': 'LOW', 'MEDIUM': 'MEDIUM', 'HIGH': 'HIGH', 'CRITICAL': 'CRITICAL'}.get(risk, risk)
    lines.append(f"## Overall Risk: **{emoji}** (Score: {scored['total_score']})")
    lines.append(f"- **{scored['red_flags']}** RED FLAGs, **{scored['warnings']}** WARNINGs")
    lines.append(f"> {scored['recommendation']}")
    lines.append(f"")
    
    lines.append(f"## Evidence Summary")
    lines.append(f"| # | Source | Method | Verdict | Detail |")
    lines.append(f"|---|--------|--------|---------|--------|")
    for i, item in enumerate(scored['evidence_items']):
        flag = 'RED' if 'RED FLAG' in item['verdict'] else 'WARN' if 'WARNING' in item['verdict'] else 'OK'
        detail = item['detail'][:80].replace('\n', ' ').replace('|', '/')
        lines.append(f"| {i+1} | {item['source']} | {item['method']} | {flag} | {detail} |")
    lines.append(f"")
    
    if forensics_result:
        lines.append(f"## Statistical Forensics")
        for method, result in forensics_result.get('results', {}).items():
            if isinstance(result, dict) and 'error' not in result:
                lines.append(f"### {method} — {result.get('verdict', 'N/A')}")
                for k, v in result.items():
                    if k not in ['verdict', 'method', 'detail', 'issues', 'individual_results']:
                        lines.append(f"- {k}: {v}")
                for issue in result.get('issues', []):
                    lines.append(f"- **Issue**: {issue}")
                lines.append(f"")
    
    if investigation_result:
        lines.append(f"## Investigator Signals")
        lines.append(f"**Target**: {investigation_result.get('investigation_target', 'Unknown')}")
        for method, result in investigation_result.get('results', {}).items():
            verdict = result.get('verdict', 'N/A')
            issues = result.get('issues', [])
            if issues:
                lines.append(f"### {method} — {verdict}")
                for issue in issues:
                    lines.append(f"- {issue}")
                lines.append(f"")
    
    lines.append(f"---")
    lines.append(f"*Report generated by Academic Data Forensics Toolkit v2.0. Human judgment required for final determination.*")
    
    report = '\n'.join(lines)
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
    return report


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python case_builder.py <forensics_json> [investigator_json] [--output report.md]")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        forensics = json.load(f)
    
    investigation = None
    output_path = None
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == '--output' and i+1 < len(args):
            output_path = args[i+1]; i += 2
        elif not investigation:
            with open(args[i], 'r', encoding='utf-8') as f:
                investigation = json.load(f)
            i += 1
        else:
            i += 1
    
    report = generate_report(forensics, investigation, forensics.get('paper', 'Untitled'), output_path)
    if not output_path:
        print(report)
    else:
        print(f"Report saved: {output_path}")
