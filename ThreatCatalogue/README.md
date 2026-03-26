# Threat Catalogue

This folder contains the ICS Threat Catalogue produced as part of a Systematic Literature Review (SLR) on security threats in Industrial Control Systems.

---

## Files

| File | Description |
|------|-------------|
| `ICSThreatCatalogue_v1_initial.xlsx` | Original catalogue submitted with the first version of the paper. |
| `ICSThreatCatalogue_v2_revised.xlsx` | Revised and reorganised catalogue following reviewer feedback. **This is the most up-to-date version.** |

> **Latest version: `ICSThreatCatalogue_v2_revised.xlsx`**

---

## Workbook Structure (Sheets)

Each `.xlsx` file is organised into the following sheets:

| Sheet | Content |
|-------|---------|
| **Accepted** | List of papers accepted during the SLR process. Rows highlighted in **green** are papers accepted in the **first inclusion round**. The sheet also contains the **inclusion criteria** applied during the selection process. |
| **ThreatsPerAssetType** | The main threat catalogue, organised by **asset type**. Each row is a threat entry associated with a specific ICS asset class (e.g., PLC, SCADA/HMI, Field Device, Robot). |
| **ThreatsPerProtocol** | Threats listed by **industrial communication protocol** (e.g., Modbus, OPC-UA, Profinet, EtherNet/IP). Each row maps a threat to the protocol through which it can be exploited. |
| **AssetTypes** | Reference list of all **asset types** involved in the SLR. Indicates which asset types are already covered by the threat modelling methodology and which are not yet addressed. |
| **Protocols** | Reference list of all **industrial protocols** identified in the SLR. Indicates which protocols are already covered by the methodology and which remain out of scope. |

---

## Colour Coding

| Colour | Sheet | Meaning |
|--------|-------|---------|
| 🟢 Green row | **Accepted** | Paper accepted in the **first inclusion round** (no borderline case). |
| 🔴 Red row | **ThreatsPerAssetType**, **ThreatsPerProtocol** | Threat **removed** after reviewer feedback (v2 only). Kept for traceability; excluded from analysis. |

---

## Catalogue Structure

Each row in the catalogue represents one threat entry. The columns are:

| Column | Description |
|--------|-------------|
| **Asset** | ICS asset category and type (e.g., `HW.PLC`, `HW.SCADA`). |
| **Threat Name** | Descriptive name of the attack or threat. |
| **Asset Type** | ICS component affected (e.g., PLC, SCADA/HMI, Network, Field Device, Robot). |
| **Protocol** | Communication protocol involved, if applicable (e.g., Modbus, OPC-UA, Profinet). |
| **Preconditions** | Conditions that must be met for the threat to be exploitable. |
| **Postconditions** | State of the system after the threat is realised. |
| **CAPEC** | Corresponding CAPEC (Common Attack Pattern Enumeration and Classification) identifier(s). |
| **References** | Number of SLR papers that report or discuss this threat. |

---

## Reading an Entry: Examples

### Example 1 – HW.PLC sheet

| Asset | Threat Name | Description | STRIDE | Compromised |
|-------|-------------|-------------|--------|-------------|
| HW.PLC | Firmware Modification | The malicious modification or replacement of the embedded software within hardware devices. | T, D, E | self, target(hosts) |

**How to read it:**
- The threat targets a **PLC** (hardware asset class `HW.PLC`).
- It involves **Tampering** (T) with firmware, can cause **Denial of Service** (D) by bricking the device, and may lead to **Elevation of Privilege** (E) if the attacker gains full control.
- `self` means the PLC itself is compromised.
- `target(hosts)` means **all assets hosted by the PLC** are also compromised — for example, if the PLC hosts a local HMI or runs embedded logic that controls field devices, those are affected too.

### Example 2 – Red row (removed entry)

A row highlighted in red in `ICSThreatCatalogue_v2_revised.xlsx` indicates a threat that was **present in v1** but **removed after reviewer feedback** (e.g., because it were at different levels of granularity). It is retained for traceability but excluded from analysis.

---

## Versioning

| Version | File | Notes |
|---------|------|-------|
| v1 | `ICSThreatCatalogue_v1_initial.xlsx` | First submission. Original structure from the SLR. |
| v2 | `ICSThreatCatalogue_v2_revised.xlsx` | Reorganised following reviewer feedback. Includes CAPEC mapping on protocols, refined STRIDE classification, updated references, and red-highlighted removed entries. |
