"""Backup and restore module"""

import shutil
import tarfile
from pathlib import Path
from datetime import datetime

class BackupManager:
    """Manages backups of builds and configurations"""
    
    def __init__(self, config):
        self.config = config
        self.backup_dir = config.work_dir.parent / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def backup_build(self):
        """Backup current build"""
        print("[*] Creating build backup...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{self.config.os_name}_{self.config.version}_{timestamp}.tar.gz"
        backup_path = self.backup_dir / backup_name
        
        with tarfile.open(backup_path, "w:gz") as tar:
            if self.config.dist_dir.exists():
                tar.add(self.config.dist_dir, arcname="dist")
            
            # Backup config
            config_file = self.config.work_dir / "build_config.json"
            if config_file.exists():
                tar.add(config_file, arcname="config.json")
        
        print(f"[✓] Backup created: {backup_path}")
        return backup_path
    
    def restore_build(self, backup_path):
        """Restore from backup"""
        print(f"[*] Restoring from {backup_path}...")
        
        with tarfile.open(backup_path, "r:gz") as tar:
            tar.extractall(self.config.work_dir)
        
        print("[✓] Restore complete")
    
    def list_backups(self):
        """List available backups"""
        backups = sorted(self.backup_dir.glob("*.tar.gz"))
        
        print("\nAvailable backups:")
        for i, backup in enumerate(backups, 1):
            size = backup.stat().st_size / (1024 * 1024)
            print(f"  {i}. {backup.name} ({size:.1f} MB)")
        
        return backups
