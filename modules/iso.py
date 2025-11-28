"""ISO creation module"""

import subprocess
import sys
import shutil
from pathlib import Path

class ISOCreator:
    """Creates bootable ISO images"""
    
    def __init__(self, config):
        self.config = config
    
    def create_iso(self):
        """Create bootable ISO image"""
        if not self.config.create_iso:
            print("[i] ISO creation disabled")
            return
        
        print(f"[*] Creating ISO image for {self.config.os_name}...")
        
        self.config.iso_dir.mkdir(parents=True, exist_ok=True)
        
        # Prepare ISO directory structure
        self._prepare_iso_structure()
        
        # Create bootable ISO
        iso_file = self.config.work_dir / f"{self.config.os_name}_{self.config.version}_{self.config.target_arch}.iso"
        self._build_iso(iso_file)
        
        print(f"[✓] ISO created: {iso_file}")
        print(f"[i] Size: {iso_file.stat().st_size / (1024**3):.2f} GB")
    
    def _prepare_iso_structure(self):
        """Prepare ISO directory structure"""
        print("[*] Preparing ISO structure...")
        
        # Copy distribution files
        if self.config.dist_dir.exists():
            for item in self.config.dist_dir.iterdir():
                dest = self.config.iso_dir / item.name
                if item.is_dir():
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(item, dest)
                else:
                    shutil.copy2(item, dest)
        
        # Create boot structure
        self._create_boot_structure()
    
    def _create_boot_structure(self):
        """Create bootable structure"""
        boot_dir = self.config.iso_dir / "boot"
        boot_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy kernel
        kernel_src = self.config.obj_dir / "usr/src" / self.config.target_arch / "sys" / \
                     (self.config.custom_kernel_config or self.config.kernel_config) / "kernel"
        
        if kernel_src.exists():
            shutil.copy2(kernel_src, boot_dir / "kernel")
    
    def _build_iso(self, output_file):
        """Build ISO using mkisofs or similar"""
        print("[*] Building ISO image...")
        
        # Try different ISO creation tools
        tools = [
            self._build_with_mkisofs,
            self._build_with_xorriso,
            self._build_with_freebsd_release
        ]
        
        for tool in tools:
            try:
                tool(output_file)
                return
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        print("[!] No ISO creation tool available (mkisofs, xorriso, or FreeBSD release)")
        print("[i] ISO directory prepared at:", self.config.iso_dir)
    
    def _build_with_mkisofs(self, output_file):
        """Build ISO with mkisofs"""
        cmd = [
            'mkisofs',
            '-R', '-J',
            '-b', 'boot/cdboot',
            '-no-emul-boot',
            '-V', self.config.iso_volume,
            '-o', str(output_file),
            str(self.config.iso_dir)
        ]
        subprocess.run(cmd, check=True)
    
    def _build_with_xorriso(self, output_file):
        """Build ISO with xorriso"""
        cmd = [
            'xorriso',
            '-as', 'mkisofs',
            '-R', '-J',
            '-b', 'boot/cdboot',
            '-no-emul-boot',
            '-V', self.config.iso_volume,
            '-o', str(output_file),
            str(self.config.iso_dir)
        ]
        subprocess.run(cmd, check=True)
    
    def _build_with_freebsd_release(self, output_file):
        """Build ISO using FreeBSD release tools"""
        script = self.config.src_dir / "release" / self.config.target_arch / "mkisoimages.sh"
        if not script.exists():
            raise FileNotFoundError("FreeBSD mkisoimages.sh not found")
        
        cmd = [
            'sh', str(script),
            '-b', self.config.iso_label,
            str(output_file),
            str(self.config.iso_dir)
        ]
        subprocess.run(cmd, check=True)
    
    def create_memstick_image(self):
        """Create USB memstick image"""
        print("[*] Creating memstick image...")
        
        memstick_file = self.config.work_dir / f"{self.config.os_name}_{self.config.version}_{self.config.target_arch}.img"
        
        # Use FreeBSD's make release target
        cmd = [
            'make',
            '-C', str(self.config.src_dir / "release"),
            'memstick',
            f'TARGET={self.config.target_arch}',
            f'TARGET_ARCH={self.config.target_arch}'
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"[✓] Memstick image created: {memstick_file}")
        except subprocess.CalledProcessError as e:
            print(f"[!] Memstick creation failed: {e}")
