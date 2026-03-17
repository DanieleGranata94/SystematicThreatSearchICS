#!/usr/bin/env python3
"""
Threat Modeller
Performs threat modelling for ICS systems using the threat catalogue.

Logic (3 steps):
  1. Direct threats per asset: threats from ThreatsPerAssetType where
     Compromised contains 'self' -> the asset itself is compromised.
  2. Protocol threats: threats from ThreatsPerProtocol associated to
     the assets involved in a [:uses {protocol: ...}] relationship.
  3. Propagation: threats whose Compromised field references other roles
     (target(hosts), target(uses), source(connects), etc.) propagate to
     the connected assets via the graph relationships defined in the MACM.
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CATALOGUE_PATH = BASE_DIR / "Catalogs.xlsx"
INPUT_DIR = Path(__file__).resolve().parent / "input"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

# ---------------------------------------------------------------------------
# Explicit overrides for asset-type mapping.
#
# These are consulted BEFORE the catalogue is read. Use them to redirect a
# MACM type to a *different* catalogue type than the one it resolves to
# automatically, or to suppress a type entirely (value = None).
#
# The automatic mapping logic (built inside load_catalogue()) is:
#   1. If the MACM type is present verbatim in the 'Asset Types' sheet → use it.
#   2. If it appears in ASSET_TYPE_MAPPING_OVERRIDES → use that value instead.
#   3. Otherwise the type is left unmapped (threats only via propagation).
#
# ASSET_TYPE_MAPPING is populated at runtime by load_catalogue().
# ---------------------------------------------------------------------------
ASSET_TYPE_MAPPING_OVERRIDES: dict[str, str | None] = {
    # HW types present in the catalogue but mapped to a more specific ICS type:
    # (none required for now – HW.SOC, HW.PC etc. are in the catalogue directly)

    # Network types: the catalogue lists generic 'Network'; sub-types inherit it.
    "Network.LAN":      "Network",
    "Network.WAN":      "Network",
    "Network.Wired":    "Network",
    "Network.WiFi":     "Network",
    "Network.Virtual":  "Network",
    "Network.PAN":      "Network",
    "Network.RAN":      "Network",
    "Network.Core":     "Network",

    # tls has no catalogue counterpart
    # (handled in PROTOCOL_MAPPING_OVERRIDES below)
}

# ASSET_TYPE_MAPPING is built automatically from the catalogue's 'Asset Types'
# sheet merged with ASSET_TYPE_MAPPING_OVERRIDES.
ASSET_TYPE_MAPPING: dict[str, str | None] = {}

# ---------------------------------------------------------------------------
# Explicit overrides for protocol mapping.
#
# Keys are the lowercase protocol labels used in the MACM :uses relations.
# Values are the exact protocol names as they appear in ThreatsPerProtocol,
# or None to explicitly skip a protocol.
#
# The automatic mapping logic (built inside load_catalogue()) is:
#   1. Normalised exact match against catalogue protocol names.
#   2. PROTOCOL_MAPPING_OVERRIDES checked for entries not matched above.
#   3. Substring fallback (proto_lower in catalogue_key or vice-versa).
#
# PROTOCOL_MAPPING is populated at runtime by load_catalogue().
# ---------------------------------------------------------------------------
PROTOCOL_MAPPING_OVERRIDES: dict[str, str | None] = {
    "tcp": "Modbus TCP",  # generic TCP in the MACM model maps to Modbus TCP
    "tls": None,          # TLS is a transport wrapper; no catalogue threats
}

# PROTOCOL_MAPPING is built automatically from the catalogue's 'Protocols'
# sheet merged with PROTOCOL_MAPPING_OVERRIDES.
PROTOCOL_MAPPING: dict[str, str | None] = {}


# ---------------------------------------------------------------------------
# MACM parser
# ---------------------------------------------------------------------------

def parse_macm(filepath):
    """Parse a .macm (Cypher-like) file.

    Returns:
        assets   : dict  node_var -> {'name': str, 'type': str, 'id': str}
        relations: list of dicts: src, rel_type, dst, protocol (optional)
    """
    assets = {}
    relations = []

    node_pattern = re.compile(
        r'\((\w+):[^\{]+\{[^\}]*component_id:\s*\'([^\']+)\'[^\}]*'
        r'name:\s*\'([^\']+)\'[^\}]*type:\s*\'([^\']+)\'[^\}]*\}\)'
    )
    rel_pattern = re.compile(
        r'\((\w+)\)-\[:(\w+)(?:\s*\{[^\}]*protocol:\s*\'([^\']+)\'[^\}]*\})?\]->\((\w+)\)'
    )

    text = filepath.read_text(encoding="utf-8")

    for m in node_pattern.finditer(text):
        var, comp_id, name, asset_type = m.group(1), m.group(2), m.group(3), m.group(4)
        assets[var] = {"id": comp_id, "name": name, "type": asset_type}

    for m in rel_pattern.finditer(text):
        src, rel_type, protocol, dst = m.group(1), m.group(2), m.group(3), m.group(4)
        relations.append({
            "src": src,
            "rel_type": rel_type,
            "dst": dst,
            "protocol": protocol.lower() if protocol else None,
        })

    return assets, relations


# ---------------------------------------------------------------------------
# Catalogue loader
# ---------------------------------------------------------------------------

def load_mappings_from_catalogue():
    """Populate ASSET_TYPE_MAPPING and PROTOCOL_MAPPING from the catalogue.

    Strategy
    --------
    Asset types
      1. Read the 'Asset Types' sheet → collect all canonical type names.
      2. Every MACM type whose name appears verbatim in that list gets a
         self-mapping (i.e. it maps to itself).
      3. Entries in ASSET_TYPE_MAPPING_OVERRIDES are then applied on top,
         overriding or adding to the automatic mappings.

    Protocols
      1. Read the 'Protocols' sheet → collect all canonical protocol names.
      2. Build a normalised (lowercase, stripped) → canonical dict.
      3. Merge PROTOCOL_MAPPING_OVERRIDES on top (these take priority).
    """
    global ASSET_TYPE_MAPPING, PROTOCOL_MAPPING

    xl = pd.ExcelFile(CATALOGUE_PATH)

    # ------------------------------------------------------------------
    # Asset types  (sheet: 'AssetTypes', canonical name column: 'Name')
    # ------------------------------------------------------------------
    df_at = pd.read_excel(xl, sheet_name="AssetTypes")
    # The canonical type names live in the 'Name' column (e.g. 'HW.SOC',
    # 'Service.App', 'Network.LAN', …).  Fall back to second column if
    # the header is ever renamed.
    type_col = "Name" if "Name" in df_at.columns else df_at.columns[1]

    catalogue_types: set[str] = set(
        df_at[type_col].dropna()
        .astype(str)
        .str.strip()
        .pipe(lambda s: s[s.str.len() > 0])
    )

    # Self-mapping for every type that exists verbatim in the catalogue
    mapping: dict[str, str | None] = {t: t for t in catalogue_types}

    # Apply overrides (they win over the automatic self-mappings)
    mapping.update(ASSET_TYPE_MAPPING_OVERRIDES)

    ASSET_TYPE_MAPPING.update(mapping)

    # ------------------------------------------------------------------
    # Protocols  (sheet: 'Protocols', name column: 'Name')
    # ------------------------------------------------------------------
    df_pr = pd.read_excel(xl, sheet_name="Protocols")
    proto_col = "Name" if "Name" in df_pr.columns else df_pr.columns[0]

    catalogue_protocols: list[str] = (
        df_pr[proto_col].dropna()
        .astype(str)
        .str.strip()
        .pipe(lambda s: s[s.str.len() > 0])
        .tolist()
    )

    # Normalised exact match
    proto_mapping: dict[str, str | None] = {
        p.strip().lower(): p for p in catalogue_protocols
        if p and not p.startswith("Protocolli")  # skip header rows
    }

    # Apply overrides
    proto_mapping.update({k.lower(): v for k, v in PROTOCOL_MAPPING_OVERRIDES.items()})

    PROTOCOL_MAPPING.update(proto_mapping)


def load_catalogue():
    """Load 'Threat Components' and 'Threat Protocols' sheets from Catalogs.xlsx,
    and populate the global ASSET_TYPE_MAPPING / PROTOCOL_MAPPING dicts
    from the catalogue's own 'AssetTypes' and 'Protocols' sheets.
    """
    load_mappings_from_catalogue()

    df_asset = pd.read_excel(CATALOGUE_PATH, sheet_name="Threat Components")
    df_proto = pd.read_excel(CATALOGUE_PATH, sheet_name="Threat Protocols")

    df_proto["Protocol"] = df_proto["Protocol"].ffill()
    df_proto["Protocol"] = df_proto["Protocol"].str.strip()

    for df in (df_asset, df_proto):
        df["Compromised"] = (
            df["Compromised"].astype(str)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )
        df["Threat"] = df["Threat"].astype(str).str.strip()

    return df_asset, df_proto


# ---------------------------------------------------------------------------
# Helper: parse Compromised roles
# ---------------------------------------------------------------------------

def parse_compromised_roles(compromised_str):
    """Return a set of roles from a Compromised field string.

    E.g. 'self, target(hosts), source(connects)' -> {'self', 'target(hosts)', 'source(connects)'}
    """
    if not compromised_str or str(compromised_str).lower() in ("nan", ""):
        return set()
    raw = str(compromised_str).replace("sourse", "source")  # fix typo in catalogue
    parts = re.split(r",\s*", raw)
    return {p.strip() for p in parts if p.strip()}


# ---------------------------------------------------------------------------
# STEP 1 – Direct threats per asset (Compromised contains 'self')
# ---------------------------------------------------------------------------

def step1_direct_threats(assets, df_asset):
    """For each asset in the model, find catalogue threats where
    Compromised includes 'self' (the asset itself is compromised).

    If the asset's MACM type is not directly present in the catalogue,
    ASSET_TYPE_MAPPING is consulted to find the closest equivalent type.
    This ensures that asset types not modelled in the catalogue (e.g.
    HW.SOC, Service.SSH) are still evaluated against the threat catalogue
    using the most semantically similar type available.
    """
    results = defaultdict(list)

    for var, info in assets.items():
        asset_type = info["type"]

        # --- resolve catalogue type -----------------------------------------
        if asset_type in ASSET_TYPE_MAPPING:
            catalogue_type = ASSET_TYPE_MAPPING[asset_type]
            mapped_from = asset_type          # keep original for CSV traceability
        else:
            catalogue_type = asset_type
            mapped_from = None

        if catalogue_type is None:
            # No direct threat mapping; asset receives threats only via propagation
            continue

        matches = df_asset[df_asset["Asset"] == catalogue_type]
        for _, row in matches.iterrows():
            roles = parse_compromised_roles(row["Compromised"])
            if "self" in roles:
                entry = {
                    "step": 1,
                    "source": "asset_type",
                    "catalogue_type": catalogue_type,
                    "mapped_from": mapped_from,
                    "threat": row["Threat"],
                    "tid": row.get("TID", ""),
                    "stride": row.get("STRIDE", ""),
                    "compromised": row["Compromised"],
                    "description": row.get("Description", ""),
                    "precondition": row.get("PreCondition", ""),
                    "postcondition": row.get("PostCondition", ""),
                    "capec_meta": row.get("CapecMeta", ""),
                    "capec_standard": row.get("CapecStandard", ""),
                    "capec_detailed": row.get("CapecDetailed", ""),
                    "easy_of_discovery": row.get("EasyOfDiscovery", ""),
                    "easy_of_exploit": row.get("EasyOfExploit", ""),
                    "awareness": row.get("Awareness", ""),
                    "intrusion_detection": row.get("IntrusionDetection", ""),
                    "loss_of_confidentiality": row.get("LossOfConfidentiality", ""),
                    "loss_of_integrity": row.get("LossOfIntegrity", ""),
                    "loss_of_availability": row.get("LossOfAvailability", ""),
                    "loss_of_accountability": row.get("LossOfAccountability", ""),
                }
                results[var].append(entry)

    return results


# ---------------------------------------------------------------------------
# STEP 2 – Protocol threats on assets in a [:uses {protocol}] relation
# ---------------------------------------------------------------------------


def step2_protocol_threats(assets, relations, df_proto):
    """For each [:uses {protocol}] relation, find matching threats in
    ThreatsPerProtocol and assign them to the assets involved.

    Resolution order for the MACM protocol label (lowercased):
      1. Direct lookup in PROTOCOL_MAPPING (populated from the 'Protocols'
         sheet + PROTOCOL_MAPPING_OVERRIDES).  None → skip explicitly.
      2. Substring fallback inside PROTOCOL_MAPPING keys.

    Roles used:
      source(uses) -> source asset of the :uses relation
      target(uses) -> destination asset of the :uses relation
    """
    results = defaultdict(list)

    for rel in relations:
        if rel["rel_type"] != "uses" or not rel["protocol"]:
            continue

        proto_lower = rel["protocol"].strip().lower()

        # 1) Direct lookup (includes overrides and auto-mapped catalogue names)
        catalogue_proto = PROTOCOL_MAPPING.get(proto_lower, "MISSING")

        if catalogue_proto == "MISSING":
            # 2) Substring fallback
            catalogue_proto = None
            for key, canonical in PROTOCOL_MAPPING.items():
                if canonical is None:
                    continue
                if proto_lower in key or key in proto_lower:
                    catalogue_proto = canonical
                    break

        if catalogue_proto is None:
            # Explicitly skipped (e.g. tls) or no match found
            continue

        threats = df_proto[df_proto["Protocol"] == catalogue_proto]
        rel_label = (
            f"({rel['src']})-[:uses {{protocol: '{rel['protocol']}'}}]->({rel['dst']})"
        )

        for _, row in threats.iterrows():
            roles = parse_compromised_roles(row["Compromised"])
            base = {
                "step": 2,
                "source": "protocol",
                "protocol": catalogue_proto,
                "threat": row["Threat"],
                "stride": row.get("STRIDE", ""),
                "compromised": row["Compromised"],
                "description": row.get("Description", ""),
                "precondition": row.get("Precondition", row.get("PreCondition", "")),
                "postcondition": row.get("PostCondition", ""),
                "note": row.get("Note", ""),
                "relation": rel_label,
            }

            if "source(uses)" in roles:
                if rel["src"] in assets:
                    e = dict(base)
                    e["role"] = "source(uses)"
                    results[rel["src"]].append(e)

            if "target(uses)" in roles:
                if rel["dst"] in assets:
                    e = dict(base)
                    e["role"] = "target(uses)"
                    results[rel["dst"]].append(e)

    return results


# ---------------------------------------------------------------------------
# STEP 3 – Threat propagation via graph relationships
# ---------------------------------------------------------------------------

# Maps a Compromised role to (relation_type, direction).
# 'forward'  : threat on asset A propagates to B  if A -[:rel]-> B
# 'backward' : threat on asset A propagates to B  if B -[:rel]-> A
PROPAGATION_RULES = {
    "target(hosts)":    ("hosts",    "forward"),
    "target(uses)":     ("uses",     "forward"),
    "target(connects)": ("connects", "forward"),
    "source(hosts)":    ("hosts",    "backward"),
    "source(uses)":     ("uses",     "backward"),
    "source(connects)": ("connects", "backward"),
}


def step3_propagation(assets, relations, df_asset):
    """Propagate threats to connected assets via the roles in Compromised
    (excluding 'self', which is handled by Step 1).

    Example:
      HW.PLC threat with Compromised = 'self, target(hosts)'
      -> any asset B where PLC -[:hosts]-> B also receives this threat.
    """
    results = defaultdict(list)

    adj_forward  = defaultdict(lambda: defaultdict(list))  # rel -> src -> [dst]
    adj_backward = defaultdict(lambda: defaultdict(list))  # rel -> dst -> [src]
    for rel in relations:
        adj_forward[rel["rel_type"]][rel["src"]].append(rel["dst"])
        adj_backward[rel["rel_type"]][rel["dst"]].append(rel["src"])

    for var, info in assets.items():
        asset_type = info["type"]
        matches = df_asset[df_asset["Asset"] == asset_type]

        for _, row in matches.iterrows():
            roles = parse_compromised_roles(row["Compromised"])
            propagated = roles - {"self"}
            if not propagated:
                continue

            for role in propagated:
                rule = PROPAGATION_RULES.get(role)
                if not rule:
                    continue
                rel_type, direction = rule

                neighbours = (
                    adj_forward[rel_type].get(var, [])
                    if direction == "forward"
                    else adj_backward[rel_type].get(var, [])
                )

                for nb_var in neighbours:
                    if nb_var not in assets:
                        continue
                    results[nb_var].append({
                        "step": 3,
                        "source": "propagation",
                        "origin_asset": var,
                        "origin_type": asset_type,
                        "propagation_role": role,
                        "relation": rel_type,
                        "threat": row["Threat"],
                        "tid": row.get("TID", ""),
                        "stride": row.get("STRIDE", ""),
                        "compromised": row["Compromised"],
                        "description": row.get("Description", ""),
                        "precondition": row.get("PreCondition", ""),
                        "postcondition": row.get("PostCondition", ""),
                        "capec_meta": row.get("CapecMeta", ""),
                        "capec_standard": row.get("CapecStandard", ""),
                        "capec_detailed": row.get("CapecDetailed", ""),
                        "easy_of_discovery": row.get("EasyOfDiscovery", ""),
                        "easy_of_exploit": row.get("EasyOfExploit", ""),
                        "awareness": row.get("Awareness", ""),
                        "intrusion_detection": row.get("IntrusionDetection", ""),
                        "loss_of_confidentiality": row.get("LossOfConfidentiality", ""),
                        "loss_of_integrity": row.get("LossOfIntegrity", ""),
                        "loss_of_availability": row.get("LossOfAvailability", ""),
                        "loss_of_accountability": row.get("LossOfAccountability", ""),
                    })

    return results


# ---------------------------------------------------------------------------
# Merge & deduplicate
# ---------------------------------------------------------------------------

def merge_results(*result_dicts):
    """Merge multiple result dicts, deduplicating on (step, threat, role, origin)."""
    merged = defaultdict(list)
    for rd in result_dicts:
        for var, threats in rd.items():
            for t in threats:
                key = (
                    t.get("step"),
                    t.get("threat"),
                    t.get("role", ""),
                    t.get("propagation_role", ""),
                    t.get("origin_asset", ""),
                )
                existing = {
                    (e.get("step"), e.get("threat"), e.get("role", ""),
                     e.get("propagation_role", ""), e.get("origin_asset", ""))
                    for e in merged[var]
                }
                if key not in existing:
                    merged[var].append(t)
    return merged


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

STEP_LABELS = {
    1: "Step 1 – Direct threat        (Compromised: self)",
    2: "Step 2 – Protocol threat",
    3: "Step 3 – Propagated threat",
}


def print_report(assets, merged):
    print("\n" + "=" * 74)
    print("  ICS THREAT MODELLING REPORT")
    print("=" * 74)

    total = 0
    assets_hit = 0
    for var in sorted(assets, key=lambda v: assets[v]["name"]):
        info = assets[var]
        threats = merged.get(var, [])
        if not threats:
            continue
        assets_hit += 1
        print(f"\n┌─ Asset : {info['name']}  [{info['type']}]  (id={info['id']})")

        by_step = defaultdict(list)
        for t in threats:
            by_step[t["step"]].append(t)

        for step in sorted(by_step):
            print(f"│  ── {STEP_LABELS[step]} ──")
            for t in by_step[step]:
                tid = str(t.get("tid", "")).strip()
                print(f"│     • [{tid:>4}] {t['threat']}  [STRIDE: {t.get('stride','?')}]")
                if t["step"] == 2:
                    print(f"│            Protocol : {t.get('protocol','?')}")
                    print(f"│            Role     : {t.get('role','?')}")
                elif t["step"] == 3:
                    origin_name = assets.get(
                        t.get("origin_asset", ""), {}
                    ).get("name", t.get("origin_asset", ""))
                    print(f"│            From     : {origin_name} [{t.get('origin_type','')}]")
                    print(f"│            Via      : [:{t.get('relation','')}]  "
                          f"role='{t.get('propagation_role','')}'")
        total += len(threats)

    print(f"\n{'='*74}")
    print(f"  Assets with threats : {assets_hit} / {len(assets)}")
    print(f"  Total threat entries: {total}")
    print("=" * 74)


def save_report_csv(assets, merged, output_path):
    rows = []
    for var, info in assets.items():
        threats = merged.get(var, [])
        if threats:
            for t in threats:
                rows.append({
                    "asset_name":       info.get("name", ""),
                    "asset_type":       info.get("type", ""),
                    "asset_id":         info.get("id", ""),
                    "step":             t.get("step"),
                    "threat":           t.get("threat"),
                    "tid":              t.get("tid", ""),
                    "stride":           t.get("stride", ""),
                    "description":      t.get("description", ""),
                    "compromised":      t.get("compromised", ""),
                    "precondition":     t.get("precondition", ""),
                    "postcondition":    t.get("postcondition", ""),
                    "protocol":         t.get("protocol", ""),
                    "role":             t.get("role", ""),
                    "propagation_role": t.get("propagation_role", ""),
                    "origin_type":      t.get("origin_type", ""),
                    "relation_type":    t.get("relation", ""),
                })
        else:
            # Asset with zero threats – still included for completeness
            rows.append({
                "asset_name":       info.get("name", ""),
                "asset_type":       info.get("type", ""),
                "asset_id":         info.get("id", ""),
                "step":             "",
                "threat":           "NO THREATS IDENTIFIED",
                "tid":              "",
                "stride":           "",
                "description":      "",
                "compromised":      "",
                "precondition":     "",
                "postcondition":    "",
                "protocol":         "",
                "role":             "",
                "propagation_role": "",
                "origin_type":      "",
                "relation_type":    "",
            })
    df = pd.DataFrame(rows)
    df.sort_values(["asset_name", "step", "threat"], inplace=True)
    df.to_csv(output_path, index=False)
    print(f"\n[✓] CSV report saved: {output_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    macm_files = list(INPUT_DIR.glob("*.macm"))
    if not macm_files:
        print(f"[!] No .macm files found in {INPUT_DIR}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[→] Loading catalogue: {CATALOGUE_PATH.name}")
    df_asset, df_proto = load_catalogue()
    print(f"    Threat Components   : {len(df_asset)} rows")
    print(f"    Threat Protocols    : {len(df_proto)} rows")
    print(f"    Asset type mappings : {len(ASSET_TYPE_MAPPING)} types known to catalogue")
    overridden = {k: v for k, v in ASSET_TYPE_MAPPING.items()
                  if v != k or k in ASSET_TYPE_MAPPING_OVERRIDES}
    if overridden:
        print(f"    Overrides applied   : {overridden}")
    proto_overridden = {k: v for k, v in PROTOCOL_MAPPING.items()
                        if k in PROTOCOL_MAPPING_OVERRIDES}
    print(f"    Protocol mappings   : {len(PROTOCOL_MAPPING)} protocols known")
    if proto_overridden:
        print(f"    Protocol overrides  : {proto_overridden}")

    for macm_path in macm_files:
        print(f"\n[→] Model file: {macm_path.name}")
        assets, relations = parse_macm(macm_path)
        print(f"    Assets    : {len(assets)}")
        print(f"    Relations : {len(relations)}")

        step1 = step1_direct_threats(assets, df_asset)
        step2 = step2_protocol_threats(assets, relations, df_proto)
        step3 = step3_propagation(assets, relations, df_asset)

        merged = merge_results(step1, step2, step3)
        print_report(assets, merged)

        out_name = macm_path.stem + "_threat_model.csv"
        save_report_csv(assets, merged, OUTPUT_DIR / out_name)


if __name__ == "__main__":
    main()
