"""Configuration management for FreeBSD builder"""

import json
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional

@dataclass
class Config:
    """Build configuration"""
    work_dir: str
    os_name: str
    version: str
    target_arch: str
    git_repo: str = "https://github.com/freebsd/freebsd-src"
    git_branch: str = None
    kernel_config: str = "GENERIC"
    custom_kernel_config: str = None
    make_jobs: int = 4
    
    # Advanced options
    enable_ports: bool = True
    ports_repo: str = "https://git.freebsd.org/ports.git"
    custom_packages: List[str] = field(default_factory=list)
    kernel_options: List[str] = field(default_factory=list)
    kernel_devices: List[str] = field(default_factory=list)
    kernel_nodevices: List[str] = field(default_factory=list)
    
    # Customization
    custom_motd: Optional[str] = None
    custom_logo: Optional[str] = None
    custom_rc_conf: Dict[str, str] = field(default_factory=dict)
    custom_sysctl: Dict[str, str] = field(default_factory=dict)
    
    # Patches
    patch_dir: Optional[str] = None
    
    # ISO/Image creation
    create_iso: bool = False
    iso_label: str = None
    iso_volume: str = None
    
    # Cross-compilation
    cross_toolchain: Optional[str] = None
    
    # Build options
    build_options: Dict[str, str] = field(default_factory=dict)
    make_conf_additions: List[str] = field(default_factory=list)
    src_conf_additions: List[str] = field(default_factory=list)
    
    # Hooks
    pre_build_hooks: List[str] = field(default_factory=list)
    post_build_hooks: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.work_dir = Path(self.work_dir).resolve()
        self.src_dir = self.work_dir / "src"
        self.obj_dir = self.work_dir / "obj"
        self.dist_dir = self.work_dir / "dist"
        self.ports_dir = self.work_dir / "ports"
        self.iso_dir = self.work_dir / "iso"
        self.patches_dir = Path(self.patch_dir) if self.patch_dir else self.work_dir / "patches"
        
        if not self.git_branch:
            self.git_branch = f"releng/{self.version.split('-')[0]}"
        
        if not self.iso_label:
            self.iso_label = self.os_name
        
        if not self.iso_volume:
            self.iso_volume = f"{self.os_name}_{self.version}"
    
    def save_to_file(self, filepath):
        """Save config to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(asdict(self), f, indent=2, default=str)
    
    def load_from_file(self, filepath):
        """Load config from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
        self.__post_init__()
