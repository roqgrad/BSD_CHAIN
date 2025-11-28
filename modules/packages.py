"""Package management module for custom OS"""

import subprocess
import sys
from pathlib import Path

class PackageManager:
    """Manages custom packages and ports"""
    
    def __init__(self, config):
        self.config = config
    
    def setup_ports(self):
        """Clone and setup ports tree"""
        if not self.config.enable_ports:
            print("[i] Ports disabled, skipping")
            return
        
        if self.config.ports_dir.exists():
            print(f"[i] Ports directory exists: {self.config.ports_dir}")
            return
        
        print(f"[*] Cloning ports tree...")
        cmd = [
            'git', 'clone',
            '--depth', '1',
            self.config.ports_repo,
            str(self.config.ports_dir)
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"[✓] Ports cloned to {self.config.ports_dir}")
        except subprocess.CalledProcessError as e:
            print(f"[✗] Ports clone failed: {e}", file=sys.stderr)
            raise
    
    def build_custom_packages(self):
        """Build custom packages from ports"""
        if not self.config.custom_packages:
            print("[i] No custom packages specified")
            return
        
        print(f"[*] Building {len(self.config.custom_packages)} custom packages...")
        
        pkg_dir = self.config.work_dir / "packages"
        pkg_dir.mkdir(parents=True, exist_ok=True)
        
        for package in self.config.custom_packages:
            self._build_package(package, pkg_dir)
    
    def _build_package(self, package, output_dir):
        """Build a single package"""
        print(f"[*] Building package: {package}")
        
        # Find port directory
        port_path = self._find_port(package)
        if not port_path:
            print(f"[!] Port not found: {package}")
            return
        
        # Build package
        cmd = [
            'make',
            'package',
            f'PACKAGES={output_dir}'
        ]
        
        try:
            subprocess.run(cmd, cwd=port_path, check=True)
            print(f"[✓] Built: {package}")
        except subprocess.CalledProcessError as e:
            print(f"[!] Failed to build {package}: {e}")
    
    def _find_port(self, package):
        """Find port directory by name"""
        # Simple search - can be enhanced
        for category_dir in self.config.ports_dir.iterdir():
            if category_dir.is_dir():
                port_dir = category_dir / package
                if port_dir.exists():
                    return port_dir
        return None
    
    def create_package_manifest(self):
        """Create manifest of included packages"""
        manifest_file = self.config.work_dir / "package_manifest.txt"
        
        with open(manifest_file, 'w') as f:
            f.write(f"{self.config.os_name} Package Manifest\n")
            f.write("=" * 50 + "\n\n")
            
            if self.config.custom_packages:
                f.write("Custom Packages:\n")
                for pkg in self.config.custom_packages:
                    f.write(f"  - {pkg}\n")
            else:
                f.write("No custom packages\n")
        
        print(f"[i] Package manifest: {manifest_file}")
