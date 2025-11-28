"""Build hooks module"""

import subprocess
import sys
from pathlib import Path
from typing import List

class HookManager:
    """Manages pre/post build hooks"""
    
    def __init__(self, config):
        self.config = config
    
    def run_pre_build_hooks(self):
        """Run pre-build hooks"""
        if not self.config.pre_build_hooks:
            return
        
        print(f"[*] Running {len(self.config.pre_build_hooks)} pre-build hooks...")
        self._run_hooks(self.config.pre_build_hooks, "pre-build")
    
    def run_post_build_hooks(self):
        """Run post-build hooks"""
        if not self.config.post_build_hooks:
            return
        
        print(f"[*] Running {len(self.config.post_build_hooks)} post-build hooks...")
        self._run_hooks(self.config.post_build_hooks, "post-build")
    
    def _run_hooks(self, hooks: List[str], hook_type: str):
        """Execute hook scripts"""
        for i, hook in enumerate(hooks, 1):
            print(f"[*] {hook_type} hook {i}/{len(hooks)}: {hook}")
            
            # Check if it's a file or command
            hook_path = Path(hook)
            if hook_path.exists() and hook_path.is_file():
                self._run_script(hook_path)
            else:
                self._run_command(hook)
    
    def _run_script(self, script_path):
        """Run a hook script"""
        try:
            subprocess.run(
                [str(script_path)],
                cwd=self.config.work_dir,
                check=True,
                env={
                    **subprocess.os.environ.copy(),
                    'FREEBSD_SRC': str(self.config.src_dir),
                    'FREEBSD_OBJ': str(self.config.obj_dir),
                    'FREEBSD_DIST': str(self.config.dist_dir),
                    'OS_NAME': self.config.os_name,
                    'OS_VERSION': self.config.version
                }
            )
            print(f"[✓] Hook completed: {script_path.name}")
        except subprocess.CalledProcessError as e:
            print(f"[!] Hook failed: {e}", file=sys.stderr)
    
    def _run_command(self, command):
        """Run a hook command"""
        try:
            subprocess.run(
                command,
                shell=True,
                cwd=self.config.work_dir,
                check=True,
                env={
                    **subprocess.os.environ.copy(),
                    'FREEBSD_SRC': str(self.config.src_dir),
                    'FREEBSD_OBJ': str(self.config.obj_dir),
                    'FREEBSD_DIST': str(self.config.dist_dir),
                    'OS_NAME': self.config.os_name,
                    'OS_VERSION': self.config.version
                }
            )
            print(f"[✓] Hook completed: {command}")
        except subprocess.CalledProcessError as e:
            print(f"[!] Hook failed: {e}", file=sys.stderr)
