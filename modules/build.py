"""FreeBSD build module"""

import subprocess
import sys
import time
from pathlib import Path

class FreeBSDBuilder:
    """Handles building FreeBSD"""
    
    def __init__(self, config):
        self.config = config
    
    def build(self):
        """Execute full build process"""
        print(f"[*] Starting build for {self.config.os_name}")
        print(f"[*] Target: {self.config.target_arch}")
        
        # Run pre-build hooks
        from modules.hooks import HookManager
        hook_manager = HookManager(self.config)
        hook_manager.run_pre_build_hooks()
        
        start_time = time.time()
        
        # Create build directories
        self.config.obj_dir.mkdir(parents=True, exist_ok=True)
        self.config.dist_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup cross-compilation if needed
        if self.config.cross_toolchain:
            self._setup_cross_toolchain()
        
        # Build steps
        self._build_world()
        self._build_kernel()
        self._create_distribution()
        
        # Run post-build hooks
        hook_manager.run_post_build_hooks()
        
        elapsed = time.time() - start_time
        print(f"\n[✓] Build completed in {elapsed/60:.1f} minutes")
        print(f"[i] Distribution files: {self.config.dist_dir}")
    
    def _build_world(self):
        """Build world (userland)"""
        print("\n[*] Building world (this may take a while)...")
        
        cmd = [
            'make',
            f'-j{self.config.make_jobs}',
            'buildworld',
            f'TARGET={self.config.target_arch}',
            f'TARGET_ARCH={self.config.target_arch}'
        ]
        
        env = {
            'MAKEOBJDIRPREFIX': str(self.config.obj_dir)
        }
        
        self._run_build_command(cmd, env, "World build")
    
    def _build_kernel(self):
        """Build kernel"""
        print("\n[*] Building kernel...")
        
        kernel_config = self.config.custom_kernel_config or self.config.kernel_config
        
        cmd = [
            'make',
            f'-j{self.config.make_jobs}',
            'buildkernel',
            f'KERNCONF={kernel_config}',
            f'TARGET={self.config.target_arch}',
            f'TARGET_ARCH={self.config.target_arch}'
        ]
        
        env = {
            'MAKEOBJDIRPREFIX': str(self.config.obj_dir)
        }
        
        self._run_build_command(cmd, env, "Kernel build")
    
    def _create_distribution(self):
        """Create distribution files"""
        print("\n[*] Creating distribution...")
        
        cmd = [
            'make',
            'distributeworld',
            'distributekernel',
            f'KERNCONF={self.config.custom_kernel_config or self.config.kernel_config}',
            f'DISTDIR={self.config.dist_dir}',
            f'TARGET={self.config.target_arch}',
            f'TARGET_ARCH={self.config.target_arch}'
        ]
        
        env = {
            'MAKEOBJDIRPREFIX': str(self.config.obj_dir)
        }
        
        self._run_build_command(cmd, env, "Distribution creation")
    
    def _run_build_command(self, cmd, env, step_name):
        """Run a build command with error handling"""
        try:
            result = subprocess.run(
                cmd,
                cwd=self.config.src_dir,
                env={**subprocess.os.environ.copy(), **env},
                check=True,
                capture_output=False
            )
            print(f"[✓] {step_name} completed")
        except subprocess.CalledProcessError as e:
            print(f"[✗] {step_name} failed: {e}", file=sys.stderr)
            raise
    
    def clean(self):
        """Clean build artifacts"""
        print("[*] Cleaning build artifacts...")
        
        if self.config.obj_dir.exists():
            import shutil
            shutil.rmtree(self.config.obj_dir)
            print(f"[✓] Removed {self.config.obj_dir}")
        
        cmd = ['make', 'cleanworld']
        try:
            subprocess.run(cmd, cwd=self.config.src_dir, check=True)
            print("[✓] Clean completed")
        except subprocess.CalledProcessError:
            print("[i] Clean command completed with warnings")

    def _setup_cross_toolchain(self):
        """Setup cross-compilation toolchain"""
        print(f"[*] Setting up cross-compilation toolchain: {self.config.cross_toolchain}")
        
        cmd = [
            'make',
            f'-j{self.config.make_jobs}',
            'toolchain',
            f'TARGET={self.config.target_arch}',
            f'TARGET_ARCH={self.config.target_arch}'
        ]
        
        env = {
            'MAKEOBJDIRPREFIX': str(self.config.obj_dir)
        }
        
        self._run_build_command(cmd, env, "Toolchain setup")
    
    def build_release(self):
        """Build full release with ISO"""
        print("[*] Building full release...")
        
        cmd = [
            'make',
            '-C', str(self.config.src_dir / "release"),
            'release',
            f'TARGET={self.config.target_arch}',
            f'TARGET_ARCH={self.config.target_arch}',
            f'KERNCONF={self.config.custom_kernel_config or self.config.kernel_config}'
        ]
        
        env = {
            'MAKEOBJDIRPREFIX': str(self.config.obj_dir),
            'CHROOTDIR': str(self.config.work_dir / "chroot")
        }
        
        self._run_build_command(cmd, env, "Release build")
    
    def incremental_build(self):
        """Perform incremental build"""
        print("[*] Performing incremental build...")
        
        # Only rebuild changed components
        self._build_world()
        self._build_kernel()
