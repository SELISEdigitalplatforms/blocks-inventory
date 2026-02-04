#!/usr/bin/env python3
"""Compute ZAP severity counts from a ZAP XML report and write a .env file.

Usage:
    python .github/scripts/compute_zap_severity.py path/to/zap-report.xml

Writes: zap-severity.env (next to the report)
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def compute_counts(report_path: Path) -> dict:
    """Return a dict with counts for riskcodes '3','2','1','0' and 'total'."""
    tree = ET.parse(report_path)
    counts = {"3": 0, "2": 0, "1": 0, "0": 0}
    for item in tree.findall(".//alertitem"):
        rc = item.findtext("riskcode")
        if rc in counts:
            counts[rc] += 1
    counts["total"] = sum(counts.values())
    return counts


def write_env(counts: dict, out_path: Path) -> None:
    """Write the counts to an env-style file at out_path."""
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"ZAP_HIGH={counts['3']}\n")
        f.write(f"ZAP_MEDIUM={counts['2']}\n")
        f.write(f"ZAP_LOW={counts['1']}\n")
        f.write(f"ZAP_INFO={counts['0']}\n")
        f.write(f"ZAP_TOTAL={counts['total']}\n")


def main(report: str) -> int:
    p = Path(report)
    if not p.is_file():
        print(f"error: report not found: {report}", file=sys.stderr)
        return 2
    try:
        counts = compute_counts(p)
    except ET.ParseError as e:
        print(f"error: failed to parse XML: {e}", file=sys.stderr)
        return 3

    out = p.with_name("zap-severity.env")
    write_env(counts, out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "zap-report.xml"))
