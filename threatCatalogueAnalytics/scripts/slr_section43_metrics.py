#!/usr/bin/env python3
"""
Section 4.3 – Three SLR metrics for threat-asset/protocol associations.

All metrics are computed directly from the ICS Threat Catalogue
(ICSThreatCatalogue (10).xlsx), NOT from the threat model output
(which belongs to the case-study section).

Produces three PDF figures saved in threat_modelling/output/:

  fig1_coverage.pdf
      Coverage – for each asset type and protocol, the number of
      distinct papers that mention at least one threat for that
      asset/protocol (union of paper IDs across all its threat entries).

  fig2_stride_breadth.pdf
      Breadth – bar chart with STRIDE on the X-axis and the number of
      distinct threat entries in that category on the Y-axis.
      Multi-label threats (e.g. "T,E,D") are counted in every matching
      category. Covers both ThreatsPerAssetType and ThreatsPerProtocol.

  fig3_evidence_weighted.pdf
      Evidence-weighted associations – for each asset type and protocol,
      the sum of paper counts across all its threat entries (each
      threat-asset/protocol link is weighted by the number of papers
      that report that threat).

Data source: ICSThreatCatalogue (10).xlsx
  - ThreatsPerAssetType  -> asset-level threats  (column 'Reference')
  - ThreatsPerProtocol   -> protocol-level threats (column 'Reference')
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
PALETTE_BLUE   = "#1A5276"   # asset types  – fig1 coverage  (deep navy)
PALETTE_INDIGO = "#5D6D7E"   # protocols    – fig1 coverage  (slate grey)
PALETTE_TEAL   = "#1A5276"   # fig2 STRIDE                   (deep navy)
PALETTE_AMBER  = "#1A5276"   # asset types  – fig3 evidence  (deep navy)
PALETTE_ROSE   = "#5D6D7E"   # protocols    – fig3 evidence  (slate grey)
GRID_COLOR     = "#E8EAED"
TEXT_COLOR     = "#1C2833"
C_SPINE        = "#BDBDBD"

# Entries with fewer than MIN_PAPERS papers are excluded from fig1 and fig3.
MIN_PAPERS = 3

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
    "axes.labelcolor":   TEXT_COLOR,
    "xtick.color":       TEXT_COLOR,
    "ytick.color":       TEXT_COLOR,
    "xtick.major.size":  3,
    "xtick.major.width": 0.6,
    "ytick.major.size":  0,
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
    "pdf.fonttype":      42,
})

# ---------------------------------------------------------------------------
# Load catalogue
# ---------------------------------------------------------------------------

def parse_papers(ref_str):
    """Return a set of paper IDs from a comma-separated Reference string."""
    if not ref_str or str(ref_str).strip() in ("", "nan"):
        return set()
    return {p.strip() for p in str(ref_str).split(",") if p.strip()}


def load_catalogue():
    xl = pd.ExcelFile(CATALOGUE)

    # --- ThreatsPerAssetType ---
    df_a = pd.read_excel(xl, sheet_name="ThreatsPerAssetType")
    df_a["Asset"]  = df_a["Asset"].astype(str).str.strip()
    df_a["Threat"] = df_a["Threat"].astype(str).str.strip()
    df_a["STRIDE"] = df_a["STRIDE"].astype(str).str.strip()
    df_a["papers"] = df_a["Reference"].apply(parse_papers)

    # --- ThreatsPerProtocol ---
    df_p = pd.read_excel(xl, sheet_name="ThreatsPerProtocol")
    df_p["Protocol"] = df_p["Protocol"].ffill().astype(str).str.strip()
    df_p["Protocol"] = df_p["Protocol"].replace({"S7  Protocl": "S7 Protocol"})
    df_p["Threat"] = df_p["Threat"].astype(str).str.strip()
    df_p["STRIDE"] = df_p["STRIDE"].astype(str).str.strip()
    df_p["papers"] = df_p["Reference"].apply(parse_papers)

    return df_a, df_p


# ---------------------------------------------------------------------------
# Shared helper: horizontal bar chart
# ---------------------------------------------------------------------------

def hbar_chart(ax, labels, values, color, xlabel, title):
    """Horizontal bar chart, publication style with smart label placement."""
    n    = len(labels)
    ypos = range(n)
    bars = ax.barh(ypos, values,
                   height=0.65, color=color,
                   edgecolor="white", linewidth=0.5, zorder=3)

    x_max = max(values) if values else 1
    ax.set_xlim(0, x_max * 1.30)

    for bar, val in zip(bars, values):
        bw     = bar.get_width()
        cy     = bar.get_y() + bar.get_height() / 2
        inside = (bw / x_max) >= 0.55
        if inside:
            ax.text(bw - x_max * 0.03, cy, str(val),
                    va="center", ha="right",
                    fontsize=8, color="white", fontweight="bold", zorder=4)
        else:
            ax.text(bw + x_max * 0.03, cy, str(val),
                    va="center", ha="left",
                    fontsize=8, color=TEXT_COLOR, zorder=4)

    ax.set_yticks(list(ypos))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel(xlabel, labelpad=5)
    ax.set_title(title, pad=7)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True, nbins=4))
    ax.grid(axis="x", color=GRID_COLOR, linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines["left"].set_visible(False)


# ---------------------------------------------------------------------------
# FIGURE 1 – Coverage
# ---------------------------------------------------------------------------

def fig1_coverage(df_a, df_p):
    """
    For each asset type / protocol: number of distinct papers that mention
    >= 1 threat for that entity (union of paper sets across all its rows).
    Two sub-plots: one for asset types, one for protocols.
    """
    # -- asset types --
    cov_asset = defaultdict(set)
    for _, row in df_a.iterrows():
        cov_asset[row["Asset"]] |= row["papers"]

    # -- protocols --
    cov_proto = defaultdict(set)
    for _, row in df_p.iterrows():
        cov_proto[row["Protocol"]] |= row["papers"]

    # sort descending, then filter out entries with < MIN_PAPERS papers
    a_items = sorted(cov_asset.items(), key=lambda x: len(x[1]), reverse=True)
    p_items = sorted(cov_proto.items(), key=lambda x: len(x[1]), reverse=True)

    a_items = [(k, v) for k, v in a_items if len(v) >= MIN_PAPERS]
    p_items = [(k, v) for k, v in p_items if len(v) >= MIN_PAPERS]

    a_labels = [k for k, _ in a_items][::-1]
    a_vals   = [len(v) for _, v in a_items][::-1]
    p_labels = [k for k, _ in p_items][::-1]
    p_vals   = [len(v) for _, v in p_items][::-1]

    na = len(a_labels)
    np_ = len(p_labels)
    h  = max(2.2, max(na, np_) * 0.28 + 0.7)
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(6.9, h),
        gridspec_kw={"wspace": 0.55, "left": 0.22,
                     "right": 0.97, "top": 0.93, "bottom": 0.12},
    )

    hbar_chart(ax1, a_labels, a_vals, PALETTE_BLUE,
               "Distinct papers",
               "(a) Asset Types")

    hbar_chart(ax2, p_labels, p_vals, PALETTE_INDIGO,
               "Distinct papers",
               "(b) Protocols")

    out = OUT_DIR / "fig1_coverage.pdf"
    fig.savefig(out, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"[✓] Saved: {out}")


# ---------------------------------------------------------------------------
# FIGURE 2 – Breadth (STRIDE distribution)
# ---------------------------------------------------------------------------

STRIDE_LABELS = {
    "S": "Spoofing",
    "T": "Tampering",
    "R": "Repudiation",
    "I": "Information\nDisclosure",
    "D": "Denial\nof Service",
    "E": "Elevation\nof Privilege",
}
STRIDE_ORDER = ["S", "T", "R", "I", "D", "E"]


def fig2_stride_breadth(df_a, df_p):
    """
    Count distinct threat entries per STRIDE letter.
    Multi-label entries (e.g. 'T,E,D') are split; each letter gets +1.
    Covers both asset-type and protocol threats; deduplication by Threat name.
    """
    df_all = pd.concat([
        df_a[["Threat", "STRIDE"]],
        df_p[["Threat", "STRIDE"]],
    ], ignore_index=True).drop_duplicates(subset="Threat")

    stride_count = defaultdict(int)
    for _, row in df_all.iterrows():
        raw = str(row["STRIDE"]).replace(";", ",").replace(" ", ",")
        for letter in raw.split(","):
            letter = letter.strip()
            if letter in STRIDE_ORDER:
                stride_count[letter] += 1

    counts  = [stride_count.get(c, 0) for c in STRIDE_ORDER]
    xlabels = [f"{c}\n{STRIDE_LABELS[c]}" for c in STRIDE_ORDER]

    fig, ax = plt.subplots(figsize=(5.5, 2.8))
    bars = ax.bar(xlabels, counts, color=PALETTE_TEAL, edgecolor="white",
                  linewidth=0.5, width=0.52, zorder=3)

    y_max = max(counts) if counts else 1
    for bar, val in zip(bars, counts):
        cx = bar.get_x() + bar.get_width() / 2
        inside = (val / y_max) >= 0.55
        if inside:
            ax.text(cx, val - y_max * 0.04, str(val),
                    ha="center", va="top",
                    fontsize=8, color="white", fontweight="bold", zorder=4)
        else:
            ax.text(cx, val + y_max * 0.02, str(val),
                    ha="center", va="bottom",
                    fontsize=8, color=TEXT_COLOR, zorder=4)

    ax.set_ylabel("Distinct threat entries")
    ax.set_ylim(0, y_max * 1.18)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True, nbins=5))
    ax.grid(axis="y", color=GRID_COLOR, linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines["left"].set_color(GRID_COLOR)

    fig.tight_layout()
    out = OUT_DIR / "fig2_stride_breadth.pdf"
    fig.savefig(out, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"[✓] Saved: {out}")


# ---------------------------------------------------------------------------
# FIGURE 3 – Evidence-weighted associations
# ---------------------------------------------------------------------------

def fig3_evidence_weighted(df_a, df_p):
    """
    For each asset type / protocol: sum of paper counts across all threat
    entries (each threat-entity link weighted by its paper count).
    Two sub-plots: asset types and protocols.
    """
    # -- asset types --
    weight_asset = defaultdict(int)
    for _, row in df_a.iterrows():
        weight_asset[row["Asset"]] += len(row["papers"])

    # -- protocols --
    weight_proto = defaultdict(int)
    for _, row in df_p.iterrows():
        weight_proto[row["Protocol"]] += len(row["papers"])

    a_items = sorted(weight_asset.items(), key=lambda x: x[1], reverse=True)
    p_items = sorted(weight_proto.items(), key=lambda x: x[1], reverse=True)

    a_items = [(k, v) for k, v in a_items if v >= MIN_PAPERS]
    p_items = [(k, v) for k, v in p_items if v >= MIN_PAPERS]

    a_labels = [k for k, _ in a_items][::-1]
    a_vals   = [v for _, v in a_items][::-1]
    p_labels = [k for k, _ in p_items][::-1]
    p_vals   = [v for _, v in p_items][::-1]

    na  = len(a_labels)
    np_ = len(p_labels)
    h   = max(2.2, max(na, np_) * 0.28 + 0.7)
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(6.9, h),
        gridspec_kw={"wspace": 0.55, "left": 0.22,
                     "right": 0.97, "top": 0.93, "bottom": 0.12},
    )

    hbar_chart(ax1, a_labels, a_vals, PALETTE_AMBER,
               "Evidence weight",
               "(a) Asset Types")

    hbar_chart(ax2, p_labels, p_vals, PALETTE_ROSE,
               "Evidence weight",
               "(b) Protocols")

    out = OUT_DIR / "fig3_evidence_weighted.pdf"
    fig.savefig(out, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"[✓] Saved: {out}")


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

    print("\n[→] Generating Fig. 1 – Coverage …")
    fig1_coverage(df_a, df_p)

    print("[→] Generating Fig. 2 – STRIDE Breadth …")
    fig2_stride_breadth(df_a, df_p)

    print("[→] Generating Fig. 3 – Evidence-weighted associations …")
    fig3_evidence_weighted(df_a, df_p)

    print("\n[✓] All figures saved to:", OUT_DIR)


if __name__ == "__main__":
    main()
