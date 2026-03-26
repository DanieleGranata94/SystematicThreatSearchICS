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
