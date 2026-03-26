# ICS Threat Catalogue

This document describes the organisation of `ICSThreatCatalogue.xlsx`, the main artefact produced by the Systematic Literature Review (SLR) on security threats in Industrial Control Systems (ICS).

---

## Workbook Structure

The workbook contains five sheets:

| Sheet | Purpose |
|---|---|
| [Accepted Paper](#accepted-paper) | Bibliography of the papers accepted during the SLR screening phase |
| [ThreatsPerAssetType](#threatsperassettype) | Threat entries organised by ICS asset class |
| [ThreatsPerProtocol](#threatsperprotocol) | Threat entries organised by ICS communication protocol |
| [Asset Types](#asset-types) | Reference list of all asset-type identifiers and their descriptions |
| [Protocols](#protocols) | Reference list of all protocol identifiers and their descriptions |

---

## Sheet Descriptions

### Accepted Paper

Contains the metadata for the **125 papers** retained after the full-text screening phase of the SLR. The columns are drawn directly from the Scopus export format, augmented with ASReview screening labels.

Key columns:

| Column | Description |
|---|---|
| `Title` | Paper title |
| `Authors` | Author list |
| `Year` | Publication year |
| `Source title` | Journal or conference name |
| `DOI` | Digital Object Identifier |
| `Abstract` | Paper abstract |
| `Accepted` / `Rejected` | SLR inclusion decision (1 = yes) |
| `asreview_label` | ASReview automated relevance score |
| `asreview_tag_*` | Fine-grained inclusion/exclusion tags applied during screening |

---

### ThreatsPerAssetType

Contains **50 threat entries** catalogued against the ICS asset class that is directly targeted. Each row represents one threat–asset association.

#### Column Schema

| Column | Description |
|---|---|
| `TID` | Auto-generated threat identifier (e.g., `T1`, `T2`, …) |
| `Asset` | Asset-type identifier from the *Asset Types* reference sheet (e.g., `HW.PLC`) |
| `Threat` | Short name of the threat |
| `Description` | Narrative description of how the threat manifests |
| `STRIDE` | Applicable STRIDE categories (comma-separated; see [STRIDE Key](#stride-key)) |
| `Compromised` | Propagation scope: `self` (asset itself), `target(hosts)` (assets hosted by the target), `source(connects)` (upstream connected assets) |
| `PreC` / `PreI` / `PreA` | Required initial state of Confidentiality / Integrity / Availability for the attack to succeed (`p` = preserved, `f` = failed, `n` = no requirement) |
| `PreCondition` | Combined precondition vector `[C,I,A]` (derived) |
| `PostC` / `PostI` / `PostA` | Resulting state of Confidentiality / Integrity / Availability after the attack |
| `PostCondition` | Combined postcondition vector `[C,I,A]` (derived) |
| `Reference` | Comma-separated IDs of SLR papers that document this threat (keys into *Accepted Paper*) |
| `CapecMeta` | CAPEC meta-attack pattern identifier(s) |
| `CapecStandard` | CAPEC standard-attack pattern identifier(s) |
| `CapecDetailed` | CAPEC detailed-attack pattern identifier(s) |
| `RELAZIONI` | Internal modelling relations used by the threat modeller (e.g., `hosts`, `connects`, `uses`) |

#### Threats by Asset Type

| Asset Type | Description | # Threats | Threat Names |
|---|---|---|---|
| `HW.PLC` | Programmable Logic Controller | 19 | Firmware Modification, Malicious Firmware Updates, Exploitation of Known Vulnerabilities, Manipulating PLC Logic, Main Program Block Removal, Suppression/Deactivation of Alarms, Deletion/Removal of Alarms, Alarm Forgery, Input Manipulation, Memory Layout Exploitation, Credentials from Password Stores, Process Manipulation, Misconfiguration, Mode Disruption, Physical Damage, Loss of Device Control, Network Ransomware, ADC Attack, DoS Attack |
| `Service.SCADA` | Supervisory Control and Data Acquisition service | 7 | Injection of Malicious Software, Command Injection, Measurement Data Deception, Message Spoofing, Inadequate Supervisory Controls, Unauthorized Access, Remote Code Execution |
| `HW.HMI` | Human–Machine Interface terminal | 6 | Unauthorized Access, Controller Packet Tampering, Credential Cache Extraction, Fingerprinting, Operator Deception, Configuration Access |
| `HW.Actuator` | Field actuator (valve, motor, pump) | 5 | Controller Packet Tampering, Device Restart, Unauthorized Command, Unauthorized Actuation, Physical Damage |
| `HW.RTU` | Remote Terminal Unit | 4 | Malware Propagation, Covert Channel/Leakage, Modification, Physical Damage |
| `HW.IED` | Intelligent Electronic Device | 2 | Autonomous Firmware Zombie, Firmware Update Risk |
| `HW.SIS` | Safety Instrumented System | 2 | Unsafe State Allowance, Hijacking |
| `HW.Sensor` | Field sensor | 2 | Faulty/Compromised Sensor, Physical Damage |
| `Network.VPN` | VPN gateway | 1 | Unauthorized Access |
| `HW.Engineering WS` | Engineering Workstation | 1 | File Manipulation |

---

### ThreatsPerProtocol

Contains **47 threat entries** catalogued against the ICS communication protocol that is exploited. Each row represents one threat–protocol association.

#### Column Schema

| Column | Description |
|---|---|
| `Protocol` | Protocol identifier (e.g., `Modbus`, `DNP3`) |
| `Threat` | Short name of the threat |
| `Description` | Narrative description of how the threat manifests |
| `STRIDE` | Applicable STRIDE categories (comma-separated; see [STRIDE Key](#stride-key)) |
| `Compromised` | Propagation scope: `source(uses)` (the node sending protocol traffic), `target(uses)` (the node receiving it) |
| `PreC` / `PreI` / `PreA` | Required initial CIA state (`p` / `f` / `n`) |
| `Precondition` | Combined precondition vector `[C,I,A]` (derived) |
| `PostC` / `PostI` / `PostA` | Resulting CIA state after the attack |
| `PostCondition` | Combined postcondition vector `[C,I,A]` (derived) |
| `Reference` | Comma-separated SLR paper IDs |
| `CapecMeta` | CAPEC meta-attack pattern identifier(s) |
| `CapecStandard` | CAPEC standard-attack pattern identifier(s) |
| `CapecDetailed` | CAPEC detailed-attack pattern identifier(s) |

#### Threats by Protocol

| Protocol | Layer / Domain | # Threats | Threat Names |
|---|---|---|---|
| `DNP3` | Serial / Ethernet – energy & utilities | 9 | Availability Infringement, Inadequate Authentication, Lack of Robust Handling/Validation, Loss of Accountability, Transport Sequence Modification, Baseline Response Replay, Event Buffer Flooding, Passive Network Reconnaissance, Malformed Frame DoS |
| `IEC 61850` | Ethernet – substation automation | 8 | Unauthorized Supervisory Control, Sensitive Data Exposure, Unauthenticated Configuration Changes, Interruption of Automation Routines, Process Eavesdropping, Modification of MMS Packets, Dropping Legitimate MMS Packets, Injection of Malicious MMS Packets |
| `Modbus` | Serial (RS232/RS485) | 6 | Command Manipulation, Traffic Snooping, Flooding, Command Injection, Node Impersonation, Passive Reconnaissance |
| `S7 Protocol` | Ethernet – Siemens S7 PLCs | 5 | Man in the Middle, Firmware Alteration, Execution Mode Alteration, Authentication/Access Control Violation, Denial of Service |
| `Modbus TCP` | TCP/IP | 4 | Unauthorized Access, Data Tampering, Session Injection, Traffic Snooping |
| `RS485 bus` | Physical serial bus | 4 | Traffic Sniffing, Flooding, Packet Injection, Packet Modification |
| `OPC UA` | Ethernet – Industry 4.0 / IIoT | 3 | Flooding, Man in the Middle, Node Impersonation |
| `PCOM` | Serial / TCP – Unitronics PLCs | 3 | Lack of Authentication/Encryption, Command/Process Manipulation, Session Hijacking |
| `ISO TSAP` | Transport layer – S7/MMS sessions | 2 | Man in the Middle, Replay Attack |
| `PROFINET` | Ethernet – real-time factory automation | 2 | Flow Rule Blocking, False Data Injection |
| `MQTT` | TCP – IoT / IIoT messaging | 1 | MQTT Broker Information Gathering |

---

### Asset Types

A reference taxonomy containing **all asset-type identifiers** recognised by the modelling framework, together with a one-line description for each. Only the subset listed in the *ThreatsPerAssetType* sheet have associated threat entries; the remaining types are inherited from the broader MACM metamodel.

Columns: `Asset Type`, `Description`

ICS-specific asset types covered in the threat entries:

| Asset Type | Description |
|---|---|
| `HW.PLC` | Local industrial controller |
| `HW.RTU` | Remote I/O controller for field environments |
| `HW.IED` | Protection/control device in energy and automation domains |
| `HW.SIS` | Hardware for safety instrumented functions |
| `HW.HMI` | Physical terminal for operator interaction |
| `HW.Sensor` | Device that measures process variables |
| `HW.Actuator` | Device that acts on the physical process |
| `HW.Robot` | Industrial robotic equipment |
| `Service.SCADA` | Supervisory control service for industrial systems |
| `Service.MES` | Manufacturing Execution System service |

---

### Protocols

A reference list of **ICS communication protocols** together with a short technical description. Only the subset listed in the *ThreatsPerProtocol* sheet have associated threat entries; additional entries reflect protocols already covered by companion catalogues.

Columns: `Protocol`, `Description`

---

## STRIDE Key

Each threat entry is annotated with one or more STRIDE categories:

| Code | Category | Meaning |
|---|---|---|
| S | Spoofing | Impersonating another entity |
| T | Tampering | Unauthorised modification of data or code |
| R | Repudiation | Denying an action that was performed |
| I | Information Disclosure | Exposing information to unauthorised parties |
| D | Denial of Service | Disrupting availability of a resource |
| E | Elevation of Privilege | Gaining capabilities beyond those authorised |

---

## CIA Precondition / Postcondition Notation

Pre- and post-condition vectors capture the required and resulting security state for each asset dimension:

| Value | Meaning |
|---|---|
| `p` | Preserved (the property holds) |
| `f` | Failed (the property does not hold) |
| `n` | No requirement / not affected |

The combined vector is written `[C, I, A]`, for example `[p, f, n]` means Confidentiality is preserved, Integrity has failed, Availability is not relevant.

---

## CAPEC Mapping

Threats are cross-referenced to the MITRE [Common Attack Pattern Enumeration and Classification (CAPEC)](https://capec.mitre.org/) hierarchy at three levels of abstraction:

| Column | CAPEC Level |
|---|---|
| `CapecMeta` | Meta attack pattern (highest abstraction) |
| `CapecStandard` | Standard attack pattern (mid-level) |
| `CapecDetailed` | Detailed attack pattern (most specific) |

Not all entries have mappings at every level; cells are left blank where no suitable CAPEC pattern was identified.

---

## Propagation Model

The `Compromised` column encodes how a threat can propagate beyond the directly attacked asset, using the relationship types defined in the MACM system-model format:

| Value | Description |
|---|---|
| `self` | Only the directly attacked asset is compromised |
| `target(hosts)` | Assets *hosted by* the target are also compromised |
| `source(connects)` | Assets *connected upstream* of the target are also compromised |
| `source(uses)` | The asset *using* the vulnerable protocol is compromised |
| `target(uses)` | The asset *targeted* via the vulnerable protocol is compromised |

---

## Usage by Other Components

- **`threat_modelling/threat_modeller.py`** reads both *ThreatsPerAssetType* and *ThreatsPerProtocol* to build a threat model from a `.macm` system description.
- **`threatCatalogueAnalytics/scripts/generate_protocol_threats_graph.py`** reads both sheets to produce per-asset-type and per-protocol threat density figures.
- **`threatCatalogueAnalytics/scripts/slr_section43_metrics.py`** reads both sheets to produce STRIDE breadth, literature coverage, and evidence-weight figures.
