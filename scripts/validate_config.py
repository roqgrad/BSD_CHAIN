#!/usr/bin/env python3
"""Configuration validation script"""

import sys
import json
from pathlib import Path

def validate_config(config_file):
    """Validate configuration file"""
    print(f"Validating {config_file}...")
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {config_file}")
        return False
    
    errors = []
    warnings = []
    
    # Required fields
    required = ['work_dir', 'os_name', 'version', 'target_arch']
    for field in required:
        if field not in config:
            errors.append(f"Missing required field: {field}")
    
    # Validate values
    if 'target_arch' in config:
        valid_archs = ['amd64', 'arm64', 'i386', 'riscv64']
        if config['target_arch'] not in valid_archs:
            warnings.append(f"Unusual architecture: {config['target_arch']}")
    
    if 'make_jobs' in config:
        if not isinstance(config['make_jobs'], int) or config['make_jobs'] < 1:
            errors.append("make_jobs must be a positive integer")
    
    # Print results
    if errors:
        print("\n❌ Errors:")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print("\n⚠️  Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors and not warnings:
        print("✅ Configuration is valid!")
        return True
    elif not errors:
        print("\n✅ Configuration is valid (with warnings)")
        return True
    else:
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate_config.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    if not validate_config(config_file):
        sys.exit(1)
