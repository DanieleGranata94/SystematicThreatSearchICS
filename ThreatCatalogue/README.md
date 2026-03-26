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
| **Threat ID** | Unique identifier (e.g., T1, T9, T47). |
| **Threat Name** | Descriptive name of the attack or threat. |
| **Asset Type** | ICS component affected (e.g., PLC, SCADA/HMI, Network, Field Device, Robot). |
| **Protocol** | Communication protocol involved, if applicable (e.g., Modbus, OPC-UA, Profinet). |
| **STRIDE Category** | STRIDE classification: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege. Entries may belong to multiple categories. |
| **Compromised Role** | Whether the threat directly compromises the asset itself (`self`) or a connected asset. |
| **Preconditions** | Conditions that must be met for the threat to be exploitable. |
| **Postconditions** | State of the system after the threat is realised. |
| **CAPEC** | Corresponding CAPEC (Common Attack Pattern Enumeration and Classification) identifier(s). |
| **References** | Number of SLR papers that report or discuss this threat. |

---

## Versioning

| Version | File | Notes |
|---------|------|-------|
| v1 | `ICSThreatCatalogue_v1_initial.xlsx` | First submission. Original structure from the SLR. |
| v2 | `ICSThreatCatalogue_v2_revised.xlsx` | Reorganised following reviewer feedback. Includes CAPEC mapping, refined STRIDE classification, and updated references. |
