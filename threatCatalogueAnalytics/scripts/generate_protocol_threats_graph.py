#!/usr/bin/env python3
"""
Threat Density and Literature Coverage – Asset Types & Protocols.

Produces two PDF figures (saved in threat_modelling/output/):

  graph_threats_per_asset_type.pdf
      Left panel  : Threat Density  – number of threat entries per asset type.
      Right panel : Literature Coverage – number of distinct papers that
                    mention ≥1 threat for that asset type (union of paper IDs
                    from the Reference column).

  graph_threats_per_protocol.pdf
      Left panel  : Threat Density  – number of threat entries per protocol.
      Right panel : Literature Coverage – distinct papers per protocol.

Data source: ICSThreatCatalogue (10).xlsx
  ThreatsPerAssetType  (columns: Asset, Threat, STRIDE, Reference, …)
  ThreatsPerProtocol   (columns: Protocol [ffill], Threat, STRIDE, Reference, …)
"""

from pathlib import Path
from collections import defaultdict

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR  = Path(__file__).resolve().parent.parent.parent
CATALOGUE = BASE_DIR / "ICSThreatCatalogue (10).xlsx"
OUT_DIR   = BASE_DIR / "threatCatalogueAnalytics" / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Style – publication-ready (Elsevier / IEEE single-column)
# ---------------------------------------------------------------------------
C_DENSITY  = "#1A5276"   # navy   – threat density bars
C_COVERAGE = "#5D6D7E"   # slate  – literature coverage bars
C_GRID     = "#E8EAED"
C_TEXT     = "#1C2833"
C_SPINE    = "#BDBDBD"

plt.rcParams.update({
    "font.family":       "serif",
    "font.serif":        ["Times New Roman", "DejaVu Serif", "serif"],
    "font.size":         9,
    "axes.titlesize":    10,
    "axes.titleweight":  "bold",
    "axes.labelsize":    9,
    "xtick.labelsize":   8,
    "ytick.labelsize":   9,
    "axes.edgecolor":    C_SPINE,
    "axes.linewidth":    0.8,
    "axes.labelcolor":   C_TEXT,
    "xtick.color":       C_TEXT,
    "ytick.color":       C_TEXT,
    "xtick.major.size":  3,
    "xtick.major.width": 0.6,
    "ytick.major.size":  0,
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
    "pdf.fonttype":      42,   # embed fonts
})

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def parse_papers(ref_str):
    """Return a set of paper IDs from a comma-separated Reference string."""
    if not ref_str or str(ref_str).strip() in ("", "nan"):
        return set()
    return {p.strip() for p in str(ref_str).split(",") if p.strip()}


def load_catalogue():
    xl = pd.ExcelFile(CATALOGUE)

    df_a = pd.read_excel(xl, sheet_name="ThreatsPerAssetType")
    df_a["Asset"]  = df_a["Asset"].astype(str).str.strip()
    df_a["Threat"] = df_a["Threat"].astype(str).str.strip()
    df_a["papers"] = df_a["Reference"].apply(parse_papers)

    df_p = pd.read_excel(xl, sheet_name="ThreatsPerProtocol")
    df_p["Protocol"] = df_p["Protocol"].ffill().astype(str).str.strip()
    df_p["Protocol"] = df_p["Protocol"].replace({"S7  Protocl": "S7 Protocol"})
    df_p["Threat"]   = df_p["Threat"].astype(str).str.strip()
    df_p["papers"]   = df_p["Reference"].apply(parse_papers)

    return df_a, df_p


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def build_density_and_coverage(df, group_col):
    """Compute threat density and literature coverage per group."""
    density  = df.groupby(group_col).size().to_dict()
    coverage = defaultdict(set)
    for _, row in df.iterrows():
        coverage[row[group_col]] |= row["papers"]
    coverage = {k: len(v) for k, v in coverage.items()}
    order    = sorted(density, key=lambda k: density[k], reverse=True)
    return (
        {k: density[k]       for k in order},
        {k: coverage.get(k, 0) for k in order},
    )


def _hbar(ax, labels, values, color, xlabel, title,
          vline=None, annotate_inside_thresh=0.55):
    """
    Horizontal bar chart, publication style.
    Numbers are placed inside the bar when the bar is wide enough,
    outside otherwise – avoiding overlaps.
    """
    n    = len(labels)
    ypos = range(n)
    bars = ax.barh(ypos, values,
                   height=0.65, color=color,
                   edgecolor="white", linewidth=0.5,
                   zorder=3)

    x_max = max(values) if values else 1
    ax.set_xlim(0, x_max * 1.30)

    for bar, val in zip(bars, values):
        bw     = bar.get_width()
        cy     = bar.get_y() + bar.get_height() / 2
        inside = (bw / x_max) >= annotate_inside_thresh
        if inside:
            ax.text(bw - x_max * 0.03, cy, str(val),
                    va="center", ha="right",
                    fontsize=8, color="white", fontweight="bold", zorder=4)
        else:
            ax.text(bw + x_max * 0.03, cy, str(val),
                    va="center", ha="left",
                    fontsize=8, color=C_TEXT, zorder=4)

    ax.set_yticks(list(ypos))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel(xlabel, labelpad=5)
    ax.set_title(title, pad=7)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True, nbins=4))
    ax.grid(axis="x", color=C_GRID, linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines["left"].set_visible(False)

    if vline is not None:
        ax.axvline(vline, color=C_SPINE, linewidth=0.8, linestyle="--", zorder=2)


def save_dual_figure(density, coverage, entity_label, out_path):
    """
    Two-panel figure: (a) Threat Density | (b) Literature Coverage.
    Sized for a single-column journal layout (~88 mm wide → 6.9 in).
    """
    labels = list(density.keys())[::-1]   # bottom-to-top: highest on top
    d_vals = [density[k]  for k in labels]
    c_vals = [coverage[k] for k in labels]

    n   = len(labels)
    h   = max(2.2, n * 0.28 + 0.7)   # compact height
    fig, (ax1, ax2) = plt.subplots(
        1, 2,
        figsize=(6.9, h),
        gridspec_kw={"wspace": 0.05, "left": 0.28,
                     "right": 0.97, "top": 0.93, "bottom": 0.12},
    )

    _hbar(ax1, labels, d_vals, C_DENSITY,
          "Threat count", "(a) Threat Density")

    _hbar(ax2, labels, c_vals, C_COVERAGE,
          "Distinct papers", "(b) Literature Coverage")

    # Remove y-tick labels on right panel (shared axis)
    ax2.set_yticklabels([])

    fig.savefig(out_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"[✓] Saved: {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"[→] Loading catalogue: {CATALOGUE.name}")
    df_a, df_p = load_catalogue()
    print(f"    ThreatsPerAssetType : {len(df_a)} rows, "
          f"{df_a['Asset'].nunique()} asset types")
    print(f"    ThreatsPerProtocol  : {len(df_p)} rows, "
          f"{df_p['Protocol'].nunique()} protocols")

    print("\n[→] Generating graph_threats_per_asset_type.pdf …")
    density_a, coverage_a = build_density_and_coverage(df_a, "Asset")
    save_dual_figure(density_a, coverage_a,
                     "Threat Density and Literature Coverage per Asset Type",
                     OUT_DIR / "graph_threats_per_asset_type.pdf")

    print("[→] Generating graph_threats_per_protocol.pdf …")
    density_p, coverage_p = build_density_and_coverage(df_p, "Protocol")
    save_dual_figure(density_p, coverage_p,
                     "Threat Density and Literature Coverage per Protocol",
                     OUT_DIR / "graph_threats_per_protocol.pdf")

    print("\n[✓] All figures saved to:", OUT_DIR)


if __name__ == "__main__":
    main()
