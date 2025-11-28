#!/usr/bin/env python3
"""
Install additional development tools
"""

import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd):
    """Run command and return success status"""
    try:
        subprocess.run(cmd, check=True, shell=isinstance(cmd, str))
        return True
    except subprocess.CalledProcessError:
        return False

def install_rust():
    """Install Rust toolchain"""
    print("[*] Installing Rust...")
    if shutil.which('rustc'):
        print("[✓] Rust already installed")
        return
    
    if run_command('curl --proto "=https" --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y'):
        print("[✓] Rust installed")
    else:
        print("[!] Rust installation failed")

def install_go():
    """Install Go"""
    print("[*] Installing Go...")
    if shutil.which('go'):
        print("[✓] Go already installed")
        return
    
    # This is platform-specific, adjust as needed
    if run_command(['sudo', 'apt-get', 'install', '-y', 'golang-go']):
        print("[✓] Go installed")
    elif run_command(['sudo', 'pkg', 'install', '-y', 'go']):
        print("[✓] Go installed")
    else:
        print("[!] Go installation failed")

def install_node():
    """Install Node.js"""
    print("[*] Installing Node.js...")
    if shutil.which('node'):
        print("[✓] Node.js already installed")
        return
    
    if run_command(['sudo', 'apt-get', 'install', '-y', 'nodejs', 'npm']):
        print("[✓] Node.js installed")
    elif run_command(['sudo', 'pkg', 'install', '-y', 'node', 'npm']):
        print("[✓] Node.js installed")
    else:
        print("[!] Node.js installation failed")

def install_additional_python_tools():
    """Install additional Python development tools"""
    print("[*] Installing additional Python tools...")
    
    tools = [
        'ipdb',           # Debugger
        'autopep8',       # Auto-formatter
        'isort',          # Import sorter
        'bandit',         # Security linter
        'safety',         # Dependency checker
        'pre-commit',     # Git hooks
    ]
    
    pip_cmd = 'venv/bin/pip' if Path('venv').exists() else 'pip3'
    
    for tool in tools:
        if run_command([pip_cmd, 'install', tool]):
            print(f"[✓] Installed {tool}")
        else:
            print(f"[!] Failed to install {tool}")

def main():
    """Main entry point"""
    print("Additional Tools Installer")
    print("=" * 60)
    
    print("\nSelect tools to install:")
    print("1. Rust")
    print("2. Go")
    print("3. Node.js")
    print("4. Additional Python tools")
    print("5. All of the above")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-5): ").strip()
    
    if choice == '1':
        install_rust()
    elif choice == '2':
        install_go()
    elif choice == '3':
        install_node()
    elif choice == '4':
        install_additional_python_tools()
    elif choice == '5':
        install_rust()
        install_go()
        install_node()
        install_additional_python_tools()
    elif choice == '0':
        print("Exiting...")
        return
    else:
        print("Invalid choice")
        sys.exit(1)
    
    print("\n[✓] Installation complete!")

if __name__ == '__main__':
    main()
