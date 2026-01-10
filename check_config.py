#!/usr/bin/env python3
"""
Configuration Verification Script

Verifies that the environment is properly configured for ICS security research tools.
Run this script before executing any research tools to ensure proper setup.

Usage:
    python check_config.py
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Verify that the .env file exists."""
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        print("❌ .env file not found!")
        print("   Copy .env.example to .env and configure your values:")
        print("   cp .env.example .env")
        return False
    print("✅ .env file found")
    return True

def check_env_variables():
    """Verify that environment variables are properly configured."""
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent / '.env'
        load_dotenv(dotenv_path=env_path)
        
        required_vars = [
            "ROBOT_IP",
            "SCADABR_IP", 
            "PLC_IP",
            "ATTACKER_MAC",
            "TEMP_VAL"
        ]
        
        missing = []
        placeholder_values = []
        
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                missing.append(var)
            elif value in ["192.168.0.100", "192.168.0.101", "192.168.0.102", "XX:XX:XX:XX:XX:XX"]:
                placeholder_values.append(var)
        
        if missing:
            print(f"❌ Missing variables: {', '.join(missing)}")
            return False
        
        if placeholder_values:
            print(f"⚠️  The following variables still use placeholder values: {', '.join(placeholder_values)}")
            print("   Make sure to configure them with real values before use.")
        
        print("✅ All environment variables are configured")
        print("\nConfigured values:")
        for var in required_vars:
            value = os.getenv(var)
            # Mask last octets of IP and MAC for security
            if "IP" in var:
                parts = value.rsplit('.', 1)
                masked = f"{parts[0]}.XXX" if len(parts) == 2 else value
                print(f"   {var}: {masked}")
            elif "MAC" in var:
                parts = value.split(':')
                masked = ':'.join(parts[:-2] + ['XX', 'XX']) if len(parts) == 6 else value
                print(f"   {var}: {masked}")
            else:
                print(f"   {var}: {value}")
        
        return True
        
    except ImportError:
        print("❌ python-dotenv not installed")
        print("   Install with: pip install -r requirements.txt")
        return False

def check_dependencies():
    """Verify that required dependencies are installed."""
    dependencies = {
        "dotenv": "python-dotenv",
        "pyniryo": "pyniryo",
        "scapy": "scapy"
    }
    
    missing = []
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)
    
    if missing:
        print(f"\nInstall missing dependencies with:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    return True

def check_gitignore():
    """Verify that .gitignore exists and properly excludes .env."""
    gitignore_path = Path(__file__).parent / '.gitignore'
    if not gitignore_path.exists():
        print("⚠️  .gitignore file not found")
        return False
    
    with open(gitignore_path, 'r') as f:
        content = f.read()
        if '.env' in content and '.env' not in content.replace('.env/', '').replace('.env.example', ''):
            print("✅ .gitignore properly configured to exclude .env")
            return True
        else:
            # More accurate verification
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line == '.env' or line == '/.env':
                    print("✅ .gitignore properly configured to exclude .env")
                    return True
            print("⚠️  .env may not be properly excluded from git")
            return False

def main():
    print("="*60)
    print("ENVIRONMENT CONFIGURATION VERIFICATION")
    print("="*60)
    print()
    
    checks = [
        (".env file", check_env_file),
        ("Python dependencies", check_dependencies),
        ("Environment variables", check_env_variables),
        ("Git ignore configuration", check_gitignore),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking: {name}")
        print("-" * 60)
        results.append(check_func())
    
    print("\n" + "="*60)
    if all(results):
        print("✅ CONFIGURATION COMPLETE!")
        print("You can proceed with using the research tools.")
    else:
        print("⚠️  INCOMPLETE CONFIGURATION")
        print("Complete the steps indicated above before proceeding.")
        sys.exit(1)
    print("="*60)

if __name__ == "__main__":
    main()
