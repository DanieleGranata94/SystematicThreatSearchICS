#!/usr/bin/env python3
"""
run_SLRanalytics.py – Runs all analysis scripts in sequence.

Outputs produced in threat_modelling/output/:
  graph_threats_per_asset_type.pdf  – Threat Density + Literature Coverage (asset types)
  graph_threats_per_protocol.pdf    – Threat Density + Literature Coverage (protocols)
  fig1_coverage.pdf                 – Coverage (distinct papers per asset/protocol)
  fig2_stride_breadth.pdf           – Breadth (STRIDE distribution)
  fig3_evidence_weighted.pdf        – Evidence-weighted associations
"""

import runpy
from pathlib import Path

ROOT    = Path(__file__).resolve().parent
SCRIPTS = [
    ROOT / "threatCatalogueAnalytics" / "scripts" / "generate_protocol_threats_graph.py",
    ROOT / "threatCatalogueAnalytics" / "scripts" / "slr_section43_metrics.py",
]

for script in SCRIPTS:
    print(f"\n{'='*60}")
    print(f"  Running: {script.name}")
    print(f"{ '='*60}")
    runpy.run_path(str(script), run_name="__main__")

print(f"\n{'='*60}")
print("  ALL DONE")
print(f"{'='*60}")
print(f"\nOutput: {ROOT / 'threatCatalogueAnalytics' / 'output'}")
