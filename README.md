# Systematic Threat Search in Industrial Control Systems

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

This repository contains the artifacts of a Systematic Literature Review (SLR) on security threats in Industrial Control Systems (ICS). It includes a structured threat catalogue, an automated threat modelling tool, analytics scripts for generating publication-ready figures, and two proof-of-concept scripts that demonstrate vulnerabilities in Modbus/TCP and industrial robot control protocols.

All scripts are intended for security research and authorized testing only.

---

## Repository Structure

```
SystematicThreatSearchICS/
|
|-- ThreatCatalogue/
|   |-- ICSThreatCatalogue_v1_initial.xlsx   # Catalogue - first submission
|   |-- ICSThreatCatalogue_v2_revised.xlsx   # Catalogue - revised version (latest)
|   +-- README.md                            # Catalogue structure and versioning
|
|-- SLR/
|   +-- ICSRelevant.xlsx               # Papers selected during the SLR process
|
|-- threat_modelling/
|   |-- threat_modeller.py             # Automated threat modelling from a system model
|   |-- input/
|   |   +-- ics.macm                   # Example ICS system model (Pennet case study)
|   +-- output/
|       +-- ics_threat_model.csv       # Generated threat model (CSV)
|
|-- threatCatalogueAnalytics/
|   |-- scripts/
|   |   |-- generate_protocol_threats_graph.py   # Threat density and literature coverage figures
|   |   +-- slr_section43_metrics.py             # SLR metrics figures (coverage, STRIDE, evidence)
|   +-- output/
|       |-- graph_threats_per_asset_type.pdf
|       |-- graph_threats_per_protocol.pdf
|       |-- fig1_coverage.pdf
|       |-- fig2_stride_breadth.pdf
|       +-- fig3_evidence_weighted.pdf
|
|-- Scripts/
|   |-- ModbusInjector.py              # PoC: MITM attack on Modbus/TCP
|   +-- replay_from_capture.py         # PoC: replay attack on Niryo industrial robot
|
|-- Results/
|   |-- ICS2_attack_plan.xlsx          # Attack plan for the ICS2 case study
|   +-- ICS2_threat_model.xlsx         # Threat model for the ICS2 case study
|
|-- check_config.py                    # Verifies environment before running PoC scripts
|-- run_SLRanalytics.py                # Runs all analytics scripts in sequence
|-- run_all.py                         # Deprecated alias for run_SLRanalytics.py
|-- requirements.txt                   # Python dependencies
+-- .env.example                       # Configuration template
```

---

## Threat Catalogue

The catalogue is stored in `ThreatCatalogue/`. The latest version is `ICSThreatCatalogue_v2_revised.xlsx`. See [`ThreatCatalogue/README.md`](ThreatCatalogue/README.md) for a full description of the structure, columns, and versioning.

The catalogue covers the following asset classes:

- **PLC** (Programmable Logic Controller) - logic manipulation, firmware attacks, mode disruption
- **SCADA / HMI** - process manipulation, credential theft, misconfiguration
- **Network** - Man-in-the-Middle, DoS, ransomware, ARP-based attacks
- **Field Devices** - sensor input manipulation, physical damage, ADC attacks
- **Robot Systems** - replay attacks, loss of control, authentication weaknesses

Each threat entry includes: threat name, STRIDE category, asset or protocol affected, compromised role, preconditions, postconditions, CAPEC identifiers, and literature references.

---

## Scripts

### threat_modelling/threat_modeller.py

Reads a system model in `.macm` format and generates a threat model by applying the catalogue in three steps:

1. **Direct threats** - threats that directly compromise the asset itself (`Compromised: self`).
2. **Protocol threats** - threats associated with the protocols used in the system's relationships (`:uses` edges).
3. **Propagation** - threats that spread to connected assets via graph relationships (`hosts`, `uses`, `connects`).

Results are deduplicated and written to a CSV file in `threat_modelling/output/`.

**Input:** any `.macm` file placed in `threat_modelling/input/`
**Output:** `threat_modelling/output/<model_name>_threat_model.csv`

```bash
python threat_modelling/threat_modeller.py
```

---

### threatCatalogueAnalytics/scripts/generate_protocol_threats_graph.py

Reads the threat catalogue and produces two PDF figures:

- `graph_threats_per_asset_type.pdf` - two side-by-side panels: (a) number of threat entries per asset type; (b) number of distinct papers that document at least one threat for that asset type.
- `graph_threats_per_protocol.pdf` - the same two panels, broken down by protocol instead of asset type.

**Output directory:** `threatCatalogueAnalytics/output/`

This script is called automatically by `run_SLRanalytics.py`.

---

### threatCatalogueAnalytics/scripts/slr_section43_metrics.py

Reads the threat catalogue and produces three PDF figures for the SLR metrics section:

- `fig1_coverage.pdf` - for each asset type and protocol, the number of distinct papers that mention at least one threat (coverage).
- `fig2_stride_breadth.pdf` - number of distinct threat entries per STRIDE category (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege). Multi-label entries are split and counted in each matching category.
- `fig3_evidence_weighted.pdf` - for each asset type and protocol, the sum of paper counts across all threat entries (each threat-entity association weighted by the number of papers that report it).

Entries with fewer than 3 supporting papers are excluded from figures 1 and 3.

**Output directory:** `threatCatalogueAnalytics/output/`

This script is called automatically by `run_SLRanalytics.py`.

---

### run_SLRanalytics.py

Runs `generate_protocol_threats_graph.py` and `slr_section43_metrics.py` in sequence and prints a summary when done.

```bash
python run_SLRanalytics.py
```

---

### run_all.py

Deprecated. Kept for backward compatibility. Delegates to `run_SLRanalytics.py`.

---

### check_config.py

Verifies that the environment is ready before running the proof-of-concept scripts. Checks:

- the `.env` file exists
- all required Python packages are installed
- all required environment variables are set and not left at placeholder values
- `.gitignore` is configured to exclude `.env`

```bash
python check_config.py
```

---

### Scripts/ModbusInjector.py

**Purpose:** proof-of-concept Man-in-the-Middle attack on Modbus/TCP.

The script positions the attacker between a SCADA system and a PLC using ARP cache poisoning. It then intercepts Modbus/TCP traffic on port 502, modifies the payload of Read Holding Register responses (Function Code 0x03) by overwriting the register value with a configured fake value, recalculates checksums, and forwards the modified packet. The SCADA system receives falsified sensor readings without any visible disruption to the connection.

On exit (Ctrl+C), ARP tables are automatically restored.

**Vulnerabilities demonstrated:**
- Modbus/TCP carries no encryption or authentication
- Register values can be silently overwritten in transit
- No integrity or freshness verification is present in the protocol

**Requirements:** root privileges, isolated test network, Intel AX211 network adapter (or modify the interface selection logic at the top of the script).

```bash
sudo python Scripts/ModbusInjector.py
```

---

### Scripts/replay_from_capture.py

**Purpose:** proof-of-concept replay attack on a Niryo industrial robot.

The script connects to a Niryo robot via the official PyNiryo API and replays a sequence of commands extracted from a previously captured network session. The sequence includes: automatic calibration, tool detection, conveyor and I/O queries, camera settings, and a series of pose movements. No authentication bypass is required because the robot API does not enforce session authentication.

The script asks for confirmation before executing and warns the operator to clear the robot workspace.

**Vulnerabilities demonstrated:**
- The robot control API has no command authentication
- No session management or replay protection is in place
- A captured session can be replayed without credentials

```bash
python Scripts/replay_from_capture.py
```

---

## Installation

**Requirements:**
- Linux (Ubuntu 20.04 or later recommended)
- Python 3.8 or higher
- Root/administrator privileges (required for `ModbusInjector.py`)
- An isolated test environment with ICS devices

**Steps:**

```bash
# Clone the repository
git clone https://github.com/[your-username]/SystematicThreatSearchICS.git
cd SystematicThreatSearchICS

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Dependencies** (`requirements.txt`):

| Package | Purpose |
|---|---|
| `scapy` | Packet capture and manipulation (ModbusInjector) |
| `pyniryo` | Niryo robot control API (replay_from_capture) |
| `python-dotenv` | Environment variable loading from `.env` |

For the analytics scripts, also install:

```bash
pip install pandas matplotlib openpyxl
```

---

## Configuration

The proof-of-concept scripts read network parameters from a `.env` file in the project root. This keeps sensitive addresses out of version control.

```bash
cp .env.example .env
# Edit .env with your test environment values
```

**Variables:**

| Variable | Description |
|---|---|
| `ROBOT_IP` | IP address of the target Niryo robot |
| `SCADABR_IP` | IP address of the SCADA system |
| `PLC_IP` | IP address of the PLC |
| `ATTACKER_MAC` | MAC address of the attacker machine |
| `TEMP_VAL` | Integer value to inject into Modbus registers |

After editing, verify the configuration:

```bash
python check_config.py
```

The `.env` file is excluded from Git by `.gitignore`. Never commit it.

---

## Ethical Considerations

These tools must only be used:

- In controlled laboratory environments
- On systems you own or have explicit written authorization to test
- In compliance with applicable laws and regulations

**Prohibited:**
- Unauthorized testing of any systems
- Use against production/operational systems
- Any illegal or malicious activities

Users are solely responsible for ensuring proper authorization and legal compliance.

---

## Contributing

Contributions are welcome. Please:

1. Fork the repository
2. Create a feature branch
3. Test in an isolated environment
4. Submit a pull request with a clear description

---

## Resources

### Tools Used

- **Scapy** - Packet manipulation library
- **PyNiryo** - Niryo robot Python library
- **python-dotenv** - Environment variable management

---

## License

MIT License. See [LICENSE](LICENSE) for details.
