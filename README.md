# Systematic Threat Search in Industrial Control Systems

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **Proof-of-concept tools for ICS security testing and analysis**

## 📋 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Threat Catalogue](#-threat-catalogue)
- [Tools](#tools)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Ethical Considerations](#ethical-considerations)
- [Contributing](#contributing)
- [PoC Threat Mapping (MITRE ATT&CK for ICS)](#️-poc-threat-mapping-mitre-attck-for-ics)
- [License](#license)

## 🎯 Overview

This repository contains proof-of-concept security testing tools for Industrial Control Systems (ICS). The tools demonstrate vulnerabilities in industrial protocols and control systems for security research and authorized testing purposes only.

**Included Tools:**
- **ModbusInjector.py** - Man-in-the-Middle attack tool for Modbus/TCP protocol
- **replay_from_capture.py** - Traffic replay tool for industrial robot systems

## 🗂️ Threat Catalogue

The Threat Catalogue is one of the main contributions of this repository. It provides a structured collection of security threats specific to ICS environments, developed through a Systematic Literature Review (SLR) of academic and industrial sources.

The catalogue is stored in [`ThreatCatalogue/ICSThreatCatalogue.xlsx`](ThreatCatalogue/ICSThreatCatalogue%20(9).xlsx) and covers threats affecting the following asset classes:

- **PLC (Programmable Logic Controller)** – logic manipulation, firmware attacks, mode disruption
- **SCADA/HMI** – process manipulation, credential theft, misconfiguration
- **Network** – Man-in-the-Middle, DoS, ransomware, ARP-based attacks
- **Field Devices** – sensor input manipulation, physical damage, ADC attacks
- **Robot Systems** – replay attacks, loss of control, authentication weaknesses

### Catalogue Structure

Each entry in the catalogue includes:

| Field | Description |
|-------|-------------|
| **Threat ID** | Unique identifier (e.g., T1, T9, T47) |
| **Threat Name** | Descriptive name of the attack |
| **Target Asset** | ICS component affected |
| **Attack Vector** | How the attack is carried out |
| **Impact** | Effect on confidentiality, integrity, availability |
| **CAPEC Mapping** | Corresponding CAPEC pattern(s) |
| **Notes** | Context-specific notes |

### CAPEC Mapping

All threats in the catalogue are mapped to [CAPEC (Common Attack Pattern Enumeration and Classification)](https://capec.mitre.org/) patterns. CAPEC provides a standardized taxonomy of attack patterns that describes how adversaries exploit weaknesses in systems.

The mapping is available in two formats:

- 📊 **Spreadsheet**: [`ThreatCatalogue/ICSThreatCatalogue.xlsx`](ThreatCatalogue/ICSThreatCatalogue%20(9).xlsx)
- 📄 **CSV**: [`ThreatCatalogue/threat_mapping.csv`](ThreatCatalogue/threat_mapping.csv)

The catalogue currently includes **19 threats** covering attack categories such as firmware manipulation, logic alteration, alarm suppression, credential theft, process manipulation, denial of service, and replay attacks.

## 📁 Repository Structure

```
SystematicThreatSearchICS/
│
├── Scripts/                      # Security testing tools
│   ├── ModbusInjector.py        # Modbus/TCP MITM attack tool
│   └── replay_from_capture.py   # Robot command replay tool
│
├── SLR/                          # Systematic Literature Review materials
├── ThreatCatalogue/              # Threat taxonomy and categorization
│   ├── ICSThreatCatalogue.xlsx  # Full threat catalogue (19 threats)
│   └── threat_mapping.csv       # CAPEC-based threat mapping (with PoC MITRE ATT&CK examples)
├── Results/                      # Attack planning and threat models
│   ├── ICS2_attack_plan.xlsx    
│   └── ICS2_threat_model.xlsx   
│
├── .env.example                  # Configuration template
├── requirements.txt              # Python dependencies
├── check_config.py               # Configuration verification script
└── README.md                     # This file
```

## ️ Tools

### 1. ModbusInjector.py

**Purpose**: Demonstrates Man-in-the-Middle (MITM) attack on Modbus/TCP protocol

**Attack Scenario**: Intercepting and modifying sensor data between SCADA and PLC

**Technical Details**:
- ARP cache poisoning for network position
- Real-time packet interception using Scapy
- Selective payload modification (Function Code 03 - Read Holding Registers)
- Transparent forwarding to maintain connection integrity

**Demonstrated Vulnerabilities**:
- Lack of encryption in Modbus/TCP
- Absence of message authentication
- No integrity verification mechanisms
- Vulnerability to replay attacks

**Research Value**: Validates the feasibility of data integrity attacks in industrial networks without triggering obvious alerts.

### 2. replay_from_capture.py

**Purpose**: Demonstrates replay attacks on industrial robot control systems

**Attack Scenario**: Capturing and replaying legitimate robot commands without authentication

**Technical Details**:
- Network traffic capture analysis
- Command sequence extraction
- Replay via official PyNiryo API
- No authentication bypass required (vulnerability present)

**Demonstrated Vulnerabilities**:
- Lack of command authentication
- No session management
- Absence of command freshness verification
- No protection against replay attacks

**Research Value**: Highlights authentication weaknesses in modern industrial robots with network connectivity.

## 🔧 Installation

### Prerequisites

- **Operating System**: Linux (Ubuntu 20.04+ recommended) or macOS
- **Python**: 3.8 or higher
- **Privileges**: Root/Administrator access (required for packet manipulation)
- **Network**: Isolated test environment with ICS devices

### Step 1: Clone Repository

```bash
git clone https://github.com/[your-username]/SystematicThreatSearchICS.git
cd SystematicThreatSearchICS
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# .venv\Scripts\activate   # On Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Packages**:
- `scapy` - Packet manipulation and network analysis
- `pyniryo` - Niryo robot control library
- `python-dotenv` - Environment variable management

### Step 4: Verify Installation

```bash
python check_config.py
```

## ⚙️ Configuration

### Environment Variables

Configuration is managed through environment variables for:
- Safe repository sharing without exposing network details
- Easy adaptation to different test environments
- Separation of code and configuration

### Setup

1. **Copy the example configuration**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your test environment parameters**:
   ```bash
   nano .env  # or your preferred editor
   ```

3. **Required Configuration Variables**:

   ```bash
   # Robot Configuration
   ROBOT_IP=192.168.x.x          # IP address of target robot

   # Modbus Network Configuration
   SCADABR_IP=192.168.x.x        # SCADA system IP address
   PLC_IP=192.168.x.x            # PLC IP address
   ATTACKER_MAC=XX:XX:XX:XX:XX:XX # Attacker machine MAC address

   # Attack Configuration
   TEMP_VAL=1234                  # Value to inject in Modbus registers
   ```

4. **Verify Configuration**:
   ```bash
   python check_config.py
   ```

### Security Notes

⚠️ **CRITICAL**: Never commit the `.env` file to version control. It contains your actual network configuration and must remain private.

✅ The `.gitignore` file is pre-configured to exclude `.env` from Git tracking.

## 🚀 Usage

### Pre-Execution Checklist

- [ ] Isolated test environment (no production systems)
- [ ] Written authorization obtained
- [ ] Configuration verified with `check_config.py`
- [ ] Safety measures in place

### ModbusInjector

```bash
# Requires root privileges for packet manipulation
sudo python Scripts/ModbusInjector.py
```

**What it does**:
1. Performs ARP spoofing to position between SCADA and PLC
2. Intercepts Modbus/TCP traffic on port 502
3. Modifies Read Holding Register responses (Function Code 0x03)
4. Injects configured value (`TEMP_VAL`) into register data
5. Forwards modified packets maintaining connection

**Stopping**:
- Press `Ctrl+C` to stop
- ARP tables are automatically restored

### replay_from_capture

```bash
python Scripts/replay_from_capture.py
```

**What it does**:
1. Connects to robot at configured IP address
2. Executes sequence of captured commands:
   - Calibration
   - Tool updates
   - Get conveyor/tool information
   - Movement commands (joints, pose)
   - Gripper operations
3. Includes delays between commands for execution

**Safety**:
- ⚠️ Ensure robot workspace is clear
- ⚠️ Be ready to use emergency stop
- ⚠️ Robot will perform physical movements

## � Technical Details

### ModbusInjector Implementation

**ARP Spoofing Mechanism**:
```python
# Sends spoofed ARP responses to both targets
# SCADA believes attacker is the PLC
# PLC believes attacker is the SCADA
```

**Packet Modification**:
- Intercepts packets with TCP port 502
- Identifies Function Code 03 responses (Read Holding Registers)
- Modifies bytes 9-10 (register value in big-endian)
- Recalculates IP and TCP checksums
- Forwards modified packet

**Network Interface Selection**:
- Currently configured for Intel AX211 adapter
- Modify interface detection logic for other adapters

### replay_from_capture Implementation

**Command Sequence**:
The script executes a pre-captured sequence including:
- Robot calibration (`calibrate_auto()`)
- Tool detection (`update_tool()`)
- Conveyor queries (`get_connected_conveyors_id()`)
- Tool ID retrieval (`get_current_tool_id()`)
- Joint movements (`move_joints()`)
- Pose movements (`move_pose()`)
- Linear movements (`move_linear_pose()`)
- Gripper operations (`open_gripper()`, `close_gripper()`)

**Timing**:
- 0.5 second delay between commands
- Configurable via `time.sleep()` calls

## 🔒 Ethical Considerations

⚠️ **FOR AUTHORIZED SECURITY TESTING ONLY**

These tools must only be used:
- In controlled laboratory environments
- On systems you own or have explicit written authorization to test
- In compliance with applicable laws and regulations

**Prohibited**:
- Unauthorized testing of any systems
- Use against production/operational systems
- Any illegal or malicious activities

**Users are solely responsible for ensuring proper authorization and legal compliance.**

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Test in isolated environment
4. Submit pull request with clear description

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

**Note**: This software is for educational and authorized security testing only.

## 🗺️ PoC Threat Mapping (MITRE ATT&CK for ICS)

> **Note**: This mapping is **not part of the Threat Catalogue**. The catalogue uses [CAPEC](https://capec.mitre.org/) as its classification framework. The table below maps the **19 catalogue threats** to [MITRE ATT&CK for ICS](https://attack.mitre.org/matrices/ics/) techniques solely to provide a reference aligned with PLC-level attack vectors, as a support for the proof-of-concept experiments.

The full mapping is also available as a CSV file: [`ThreatCatalogue/threat_mapping.csv`](ThreatCatalogue/threat_mapping.csv)

| ID | Threat Name | Primary Technique | Secondary Technique | Notes |
|----|-------------|-------------------|---------------------|-------|
| T1 | Firmware Modification | T0857 | T0843 | T0843 applies if firmware/logic is loaded onto the PLC |
| T2 | Malicious Firmware Updates | T0857 | T0862 | |
| T3 | Exploitation of Known Vulnerabilities | T0866 | T0859 | T0859 applies if the exploit leads to use of valid credentials/accounts |
| T4 | Manipulating PLC Logic | T0834 | T0843 | |
| T5 | Main Program Block Removal | T0834 | T0814 | |
| T6 | Suppression/Deactivation of Alarms | T0878 | | |
| T7 | Deletion/Removal of Alarms | T0878 | T0834 | T0834 applies if the alarm is removed by acting on PLC logic |
| T8 | Alarm Forgery | T0878 | T0834 | T0834 applies if achieved via PLC logic modification |
| T9 | Input Manipulation | T0834 | | Mapping depends on experimental case; may involve PLC process control/manipulation techniques |
| T10 | Memory Layout Exploitation | T0888 | | |
| T11 | Credentials from Password Stores | T0847 | | |
| T12 | Process Manipulation | T0834 | | Possible association with impairment/process impact techniques |
| T13 | Misconfiguration | T0842 | T0851 | Depends on operational detail; applies when threat involves alteration of configurations/parameters |
| T14 | Mode Disruption | T0814 | | |
| T15 | Physical Damage | T0834 | | T0834 as technical cause on PLC; physical effect on the process |
| T16 | Loss of Device Control | T0814 | T0859 | T0859 applies if attacker changes passwords/credentials |
| T45 | Network Ransomware | T0821 | | Applies if data encryption/inhibition is the effect on PLC; validate against specific technique details |
| T46 | ADC Attack | T0834 | | Precise mapping depends on how the ADC attack is described; may involve PLC-specific input/process manipulation |
| T47 | DoS Attack | T0814 | | |

> **Mapping Methodology**: Threats are mapped to ATT&CK for ICS techniques based on the primary attack vector against PLC systems. Where multiple techniques apply, the principal technique is listed first. Context-dependent mappings require validation against specific experimental scenarios.

## �📚 Resources

### ICS Security Standards
- **IEC 62443** - Industrial automation security
- **NIST SP 800-82** - Guide to ICS Security
- **MITRE ATT&CK for ICS** - ICS threat knowledge base

### Tools Used
- **Scapy** - Packet manipulation library
- **PyNiryo** - Niryo robot Python library
- **python-dotenv** - Environment variable management

---

<p align="center">
  <strong>⚠️ For Authorized Security Testing Only ⚠️</strong>
</p>
