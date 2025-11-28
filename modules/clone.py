"""FreeBSD source code cloning module"""

import subprocess
import sys
from pathlib import Path

class FreeBSDCloner:
    """Handles cloning FreeBSD source code"""
    
    def __init__(self, config):
        self.config = config
    
    def clone(self):
        """Clone FreeBSD source repository"""
        self.config.work_dir.mkdir(parents=True, exist_ok=True)
        
        if self.config.src_dir.exists():
            print(f"[i] Source directory exists: {self.config.src_dir}")
            response = input("Update existing repository? (y/n): ")
            if response.lower() == 'y':
                self._update_repo()
            return
        
        print(f"[*] Cloning from {self.config.git_repo}")
        print(f"[*] Branch: {self.config.git_branch}")
        
        cmd = [
            'git', 'clone',
            '--branch', self.config.git_branch,
            '--depth', '1',
            self.config.git_repo,
            str(self.config.src_dir)
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"[✓] Cloned successfully to {self.config.src_dir}")
        except subprocess.CalledProcessError as e:
            print(f"[✗] Clone failed: {e}", file=sys.stderr)
            raise
    
    def _update_repo(self):
        """Update existing repository"""
        print("[*] Updating repository...")
        try:
            subprocess.run(
                ['git', 'pull'],
                cwd=self.config.src_dir,
                check=True
            )
            print("[✓] Repository updated")
        except subprocess.CalledProcessError as e:
            print(f"[✗] Update failed: {e}", file=sys.stderr)
            raise
