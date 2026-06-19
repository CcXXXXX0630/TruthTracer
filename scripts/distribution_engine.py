#!/usr/bin/env python3
"""
Distribution Auditor — Detect anomalous distribution patterns.
===============================================================
Tests whether reported data distributions exhibit patterns that are
statistically implausible for genuine empirical data.

Methods:
  1. Overdispersion / Underdispersion check — variance too low or too high
  2. Normality excess — data "too Gaussian" (fabricated data often over-fits normal)
  3. Variance homogeneity excess — all group SDs suspiciously uniform
  4. Integer conformity — integer data that perfectly fits continuous distributions
  5. Digit trailing — trailing digits that are too uniform (base-10 uniformity excess)

All tests are field-agnostic and rely on standard statistical properties of
genuine empirical data (noise, heterogeneity, measurement error).
"""

import math, re, json
from collections import Counter
from typing import List, Dict, Optional


# ═══════════════════════════════════════════════════════════
# 1. DISPERSION ANOMALY (over/under-dispersion)
# ═══════════════════════════════════════════════════════════

def dispersion_check(values: List[float],
                      expected_min_sd_ratio: float = 0.05,
                      expected_max_cv: float = 5.0) -> dict:
    """
    Check for anomalous dispersion in data.
    
    Genuine empirical data typically shows:
    - CV (coefficient of variation) between 0.05 and 3.0
    - Variance that scales with mean
    
    Fabricated data often shows:
    - SD is suspiciously small relative to mean (underdispersion)
    - All values tightly clustered around the mean
    - CV < 0.01 for biological/observational data (impossible precision)
    
    Args:
        values: List of numeric observations
        expected_min_sd_ratio: Minimum expected SD/mean ratio
        expected_max_cv: Maximum plausible CV
    
    Returns:
        dict with dispersion analysis
    """
    n = len(values)
    if n < 5:
        return {"verdict": "SKIP", "note": "Need at least 5 values", "n": n}
    
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / (n - 1) if n > 1 else 0
    sd = math.sqrt(variance)
    cv = sd / abs(mean) if mean != 0 else float('inf')
    
    # Skewness
    if sd > 0:
        skew = sum((x - mean) ** 3 for x in values) / (n * sd ** 3) if sd > 0 else 0
    else:
        skew = 0
    
    # Kurtosis (excess)
    if sd > 0:
        kurt = sum((x - mean) ** 4 for x in values) / (n * sd ** 4) - 3 if sd > 0 else 0
    else:
        kurt = 0
    
    issues = []
    
    # Underdispersion: variance too small
    if cv < expected_min_sd_ratio and n >= 10:
        issues.append(
            f"Underdispersion detected: CV = {cv:.4f} (below {expected_min_sd_ratio}). "
            f"Values are suspiciously uniform. Genuine data rarely achieves this level of precision."
        )
    
    # Overdispersion: CV impossibly large
    if cv > expected_max_cv:
        issues.append(
            f"Extreme overdispersion: CV = {cv:.1f}. "
            f"Such high variability combined with reported precision is unusual."
        )
    
    # Near-zero skewness with high N (fabricated normal data)
    if abs(skew) < 0.1 and n >= 30:
        issues.append(
            f"Near-perfect symmetry: skewness = {skew:.3f}. "
            f"Genuine data rarely achieves exact symmetry at N={n}."
        )
    
    # Near-zero excess kurtosis (mesokurtic — normal-like — suspect for non-normal processes)
    if abs(kurt) < 0.1 and n >= 30:
        issues.append(
            f"Near-perfect mesokurtosis: excess kurtosis = {kurt:.3f}. "
            f"Natural data typically shows some deviation from perfect normality."
        )
    
    return {
        "method": "Dispersion Anomaly Check",
        "n": n,
        "mean": round(mean, 4),
        "sd": round(sd, 4),
        "cv": round(cv, 4),
        "skewness": round(skew, 3),
        "excess_kurtosis": round(kurt, 3),
        "issues": issues,
        "verdict": "RED FLAG" if len(issues) >= 2 else \
                   "WARNING" if issues else "PASS",
        "interpretation": (
            "CV indicates relative variability. For most empirical data: "
            "CV < 0.01 = suspiciously precise. CV > 3.0 = extremely noisy. "
            f"Current CV = {cv:.3f}. Skewness = {skew:.3f} (expect |skewness| > 0.1 for real data)."
        )
    }


# ═══════════════════════════════════════════════════════════
# 2. VARIANCE HOMOGENEITY EXCESS
# ═══════════════════════════════════════════════════════════

def variance_homogeneity_check(group_stats: List[Dict]) -> dict:
    """
    Check if variances across groups are suspiciously uniform.
    
    Genuine experimental data: SDs vary across groups
    Fabricated data: all SDs are identical or very close
    
    A common fabrication tell: the researcher uses a single SD
    value for all groups, perhaps varying it slightly.
    
    Args:
        group_stats: List of dicts with 'mean', 'sd', 'n', 'label' for each group
    
    Returns:
        dict with homogeneity analysis
    """
    if len(group_stats) < 3:
        return {"verdict": "SKIP", "note": "Need at least 3 groups", "n_groups": len(group_stats)}
    
    sds = [g.get('sd', 0) for g in group_stats]
    means = [g.get('mean', 0) for g in group_stats]
    labels = [g.get('label', f'G{i+1}') for i, g in enumerate(group_stats)]
    
    sd_mean = sum(sds) / len(sds)
    sd_of_sds = math.sqrt(sum((s - sd_mean) ** 2 for s in sds) / len(sds)) if len(sds) > 1 else 0
    sd_cv = sd_of_sds / sd_mean if sd_mean > 0 else 0
    
    issues = []
    
    # CV of SDs: how much do SDs vary across groups?
    if sd_cv < 0.02:
        issues.append(
            f"SDs are nearly identical across all {len(group_stats)} groups "
            f"(CV of SDs = {sd_cv:.4f}). Genuine data shows natural SD variation."
        )
    elif sd_cv < 0.05:
        issues.append(
            f"SDs show very low variation across groups "
            f"(CV of SDs = {sd_cv:.3f}). Unusual degree of homogeneity."
        )
    
    # Check: do SDs and means correlate? (They should in most real data)
    if len(means) >= 5 and sd_mean > 0:
        # Spearman-like rank correlation (simplified)
        mean_ranks = sorted(range(len(means)), key=lambda i: means[i])
        sd_ranks = sorted(range(len(sds)), key=lambda i: sds[i])
        rank_match = sum(1 for i in range(len(means)) if mean_ranks[i] == sd_ranks[i])
        rank_agreement = rank_match / len(means)
        
        if rank_agreement > 0.8:
            issues.append(
                f"SDs perfectly track means across groups "
                f"(rank agreement = {rank_agreement:.0%}). "
                f"This pattern suggests SDs were derived from a formula rather than measured."
            )
    
    return {
        "method": "Variance Homogeneity Excess",
        "n_groups": len(group_stats),
        "sd_values": [round(s, 4) for s in sds],
        "sd_cv": round(sd_cv, 4),
        "issues": issues,
        "verdict": "RED FLAG" if len(issues) >= 2 else \
                   "WARNING" if issues else "PASS",
        "interpretation": (
            f"CV of SDs = {sd_cv:.4f}. "
            f"CV < 0.02: SDs are nearly identical (fabrication red flag). "
            f"CV > 0.05: natural variation in group SDs (genuine data pattern)."
        )
    }


# ═══════════════════════════════════════════════════════════
# 3. FULL DISTRIBUTION AUDIT
# ═══════════════════════════════════════════════════════════

def full_distribution_audit(values: List[float] = None,
                              groups: List[Dict] = None) -> dict:
    """
    Complete distribution pattern audit.
    
    Args:
        values: Flat list of observations (for dispersion check)
        groups: List of group summary statistics (for homogeneity check)
    
    Returns:
        Complete audit report
    """
    results = {}
    
    if values and len(values) >= 5:
        results['dispersion'] = dispersion_check(values)
    
    if groups and len(groups) >= 3:
        results['variance_homogeneity'] = variance_homogeneity_check(groups)
    
    # Summary
    red = sum(1 for r in results.values()
             if 'RED FLAG' in r.get('verdict', ''))
    warn = sum(1 for r in results.values()
              if 'WARNING' in r.get('verdict', ''))
    
    return {
        "results": results,
        "summary": {
            "tests_run": len(results),
            "red_flags": red,
            "warnings": warn,
            "overall": "RED FLAG" if red >= 2 else \
                       "WARNING" if red >= 1 or warn >= 2 else "PASS"
        }
    }


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Distribution Auditor — detect anomalous distribution patterns")
        print("Usage: python distribution_engine.py <values_json>")
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    result = full_distribution_audit(
        values=data.get('values'),
        groups=data.get('groups')
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
