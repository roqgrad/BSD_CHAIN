"""Patch management module"""

import subprocess
import sys
from pathlib import Path

class PatchManager:
    """Manages source code patches"""
    
    def __init__(self, config):
        self.config = config
        self.applied_patches = []
    
    def apply_patches(self):
        """Apply all patches from patch directory"""
        if not self.config.patches_dir.exists():
            print("[i] No patches directory found")
            return
        
        patch_files = sorted(self.config.patches_dir.glob("*.patch"))
        
        if not patch_files:
            print("[i] No patches to apply")
            return
        
        print(f"[*] Applying {len(patch_files)} patches...")
        
        for patch_file in patch_files:
            self._apply_patch(patch_file)
        
        self._save_patch_log()
    
    def _apply_patch(self, patch_file):
        """Apply a single patch file"""
        print(f"[*] Applying: {patch_file.name}")
        
        cmd = [
            'patch',
            '-p0',
            '-d', str(self.config.src_dir),
            '-i', str(patch_file)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            print(f"[✓] Applied: {patch_file.name}")
            self.applied_patches.append({
                'file': patch_file.name,
                'status': 'success',
                'output': result.stdout
            })
        except subprocess.CalledProcessError as e:
            print(f"[!] Failed to apply {patch_file.name}: {e}")
            self.applied_patches.append({
                'file': patch_file.name,
                'status': 'failed',
                'error': e.stderr
            })
    
    def create_patch(self, description, files=None):
        """Create a patch from current changes"""
        print(f"[*] Creating patch: {description}")
        
        patch_name = description.replace(' ', '_').lower() + '.patch'
        patch_file = self.config.patches_dir / patch_name
        
        self.config.patches_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = ['git', 'diff']
        if files:
            cmd.extend(files)
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.config.src_dir,
                check=True,
                capture_output=True,
                text=True
            )
            
            patch_file.write_text(result.stdout)
            print(f"[✓] Patch created: {patch_file}")
        except subprocess.CalledProcessError as e:
            print(f"[!] Failed to create patch: {e}")
    
    def _save_patch_log(self):
        """Save log of applied patches"""
        log_file = self.config.work_dir / "patches_applied.log"
        
        with open(log_file, 'w') as f:
            f.write(f"{self.config.os_name} Applied Patches\n")
            f.write("=" * 50 + "\n\n")
            
            for patch in self.applied_patches:
                f.write(f"Patch: {patch['file']}\n")
                f.write(f"Status: {patch['status']}\n")
                if patch['status'] == 'success':
                    f.write(f"Output: {patch.get('output', 'N/A')}\n")
                else:
                    f.write(f"Error: {patch.get('error', 'N/A')}\n")
                f.write("\n")
        
        print(f"[i] Patch log: {log_file}")
