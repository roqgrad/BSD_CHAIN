"""Security hardening and signing module"""

import subprocess
import hashlib
from pathlib import Path

class SecurityHardener:
    """Applies security hardening to the OS"""
    
    def __init__(self, config):
        self.config = config
        self.hardening_applied = []
    
    def apply_hardening(self):
        """Apply all security hardening"""
        print("[*] Applying security hardening...")
        
        self._harden_kernel()
        self._harden_sysctl()
        self._harden_rc_conf()
        self._configure_firewall()
        
        self._save_hardening_log()
        print("[✓] Security hardening applied")
    
    def _harden_kernel(self):
        """Add security kernel options"""
        security_options = [
            "MAC",              # Mandatory Access Control
            "MAC_BIBA",         # Biba integrity policy
            "MAC_LOMAC",        # Low-watermark MAC policy
            "AUDIT",            # Security event auditing
            "CAPABILITIES",     # Capability mode
        ]
        
        if not hasattr(self.config, 'kernel_options'):
            self.config.kernel_options = []
        
        for opt in security_options:
            if opt not in self.config.kernel_options:
                self.config.kernel_options.append(opt)
        
        self.hardening_applied.append("Kernel: MAC, AUDIT, CAPABILITIES")
    
    def _harden_sysctl(self):
        """Add security sysctl settings"""
        security_sysctl = {
            "security.bsd.see_other_uids": "0",
            "security.bsd.see_other_gids": "0",
            "security.bsd.unprivileged_read_msgbuf": "0",
            "security.bsd.unprivileged_proc_debug": "0",
            "kern.randompid": "1",
        }
        
        if not hasattr(self.config, 'custom_sysctl'):
            self.config.custom_sysctl = {}
        
        self.config.custom_sysctl.update(security_sysctl)
        self.hardening_applied.append("Sysctl: Process isolation, random PID")

    def _harden_rc_conf(self):
        """Add security rc.conf settings"""
        security_rc = {
            "clear_tmp_enable": "YES",
            "icmp_drop_redirect": "YES",
            "icmp_log_redirect": "YES",
        }
        
        if not hasattr(self.config, 'custom_rc_conf'):
            self.config.custom_rc_conf = {}
        
        self.config.custom_rc_conf.update(security_rc)
        self.hardening_applied.append("rc.conf: Secure defaults")
    
    def _configure_firewall(self):
        """Configure firewall"""
        firewall_rc = {
            "firewall_enable": "YES",
            "firewall_type": "workstation",
            "firewall_logging": "YES",
        }
        
        if not hasattr(self.config, 'custom_rc_conf'):
            self.config.custom_rc_conf = {}
        
        self.config.custom_rc_conf.update(firewall_rc)
        self.hardening_applied.append("Firewall: Enabled with logging")
    
    def _save_hardening_log(self):
        """Save hardening log"""
        log_file = self.config.work_dir / "security_hardening.log"
        with open(log_file, 'w') as f:
            f.write(f"{self.config.os_name} Security Hardening\n")
            f.write("=" * 50 + "\n\n")
            for item in self.hardening_applied:
                f.write(f"- {item}\n")

class BinarySigner:
    """Signs binaries and creates checksums"""
    
    def __init__(self, config):
        self.config = config
    
    def generate_checksums(self):
        """Generate checksums for all binaries"""
        print("[*] Generating checksums...")
        
        checksum_file = self.config.work_dir / "SHA256SUMS"
        
        with open(checksum_file, 'w') as f:
            for file_path in self.config.dist_dir.rglob('*'):
                if file_path.is_file():
                    sha256 = self._calculate_sha256(file_path)
                    rel_path = file_path.relative_to(self.config.dist_dir)
                    f.write(f"{sha256}  {rel_path}\n")
        
        print(f"[✓] Checksums saved to {checksum_file}")
    
    def _calculate_sha256(self, file_path):
        """Calculate SHA256 hash"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
