"""FreeBSD customization module"""

import re
import shutil
import subprocess
from pathlib import Path
from typing import List

class FreeBSDCustomizer:
    """Applies customizations to FreeBSD source"""
    
    def __init__(self, config):
        self.config = config
        self.customizations = []
    
    def apply_customizations(self):
        """Apply all customizations"""
        print(f"[*] Applying customizations for {self.config.os_name}")
        
        self._customize_branding()
        self._customize_kernel_config()
        self._customize_version_strings()
        self._create_custom_rc_scripts()
        self._apply_patches()
        self._customize_motd()
        self._customize_boot_logo()
        self._customize_rc_conf()
        self._customize_sysctl()
        self._customize_make_conf()
        self._customize_src_conf()
        
        # Save customization log
        self._save_customization_log()
        
        print(f"[✓] Customizations applied")
    
    def _customize_branding(self):
        """Change OS branding"""
        print("[*] Customizing branding...")
        
        # Update sys/conf/newvers.sh
        newvers_path = self.config.src_dir / "sys/conf/newvers.sh"
        if newvers_path.exists():
            content = newvers_path.read_text()
            
            # Replace FreeBSD with custom name
            content = content.replace('FreeBSD', self.config.os_name)
            content = re.sub(
                r'VENDOR="FreeBSD"',
                f'VENDOR="{self.config.os_name}"',
                content
            )
            
            newvers_path.write_text(content)
            self.customizations.append(f"Branding: {newvers_path}")
    
    def _customize_kernel_config(self):
        """Create custom kernel configuration"""
        print("[*] Creating custom kernel config...")
        
        kernel_dir = self.config.src_dir / "sys" / self.config.target_arch / "conf"
        custom_config = kernel_dir / f"{self.config.os_name.upper()}"
        
        # Copy GENERIC as base
        generic_config = kernel_dir / "GENERIC"
        if generic_config.exists():
            shutil.copy(generic_config, custom_config)
            
            # Add custom ident
            content = custom_config.read_text()
            content = re.sub(
                r'^ident\s+\w+',
                f'ident\t\t{self.config.os_name.upper()}',
                content,
                flags=re.MULTILINE
            )
            
            # Add custom options
            content += f"\n\n# {self.config.os_name} Custom Options\n"
            
            # Add kernel options from config
            for option in self.config.kernel_options:
                content += f"options\t\t{option}\n"
            
            # Add custom devices
            if self.config.kernel_devices:
                content += f"\n# {self.config.os_name} Custom Devices\n"
                for device in self.config.kernel_devices:
                    content += f"device\t\t{device}\n"
            
            # Remove devices
            if self.config.kernel_nodevices:
                content += f"\n# {self.config.os_name} Removed Devices\n"
                for device in self.config.kernel_nodevices:
                    content += f"nodevice\t{device}\n"
            
            custom_config.write_text(content)
            self.config.custom_kernel_config = self.config.os_name.upper()
            self.customizations.append(f"Kernel config: {custom_config}")
    
    def _customize_version_strings(self):
        """Update version strings throughout source"""
        print("[*] Updating version strings...")
        
        files_to_update = [
            "sys/sys/param.h",
            "lib/libc/gen/uname.c",
            "usr.bin/uname/uname.c"
        ]
        
        for file_path in files_to_update:
            full_path = self.config.src_dir / file_path
            if full_path.exists():
                content = full_path.read_text()
                content = content.replace('FreeBSD', self.config.os_name)
                full_path.write_text(content)
                self.customizations.append(f"Version string: {full_path}")
    
    def _create_custom_rc_scripts(self):
        """Create custom RC scripts"""
        print("[*] Creating custom RC scripts...")
        
        rc_dir = self.config.src_dir / "libexec/rc"
        custom_rc = rc_dir / "rc.d" / f"{self.config.os_name.lower()}_init"
        
        if rc_dir.exists():
            custom_rc.parent.mkdir(parents=True, exist_ok=True)
            
            rc_content = f"""#!/bin/sh
#
# PROVIDE: {self.config.os_name.lower()}_init
# REQUIRE: NETWORKING
# BEFORE: LOGIN

. /etc/rc.subr

name="{self.config.os_name.lower()}_init"
rcvar="{self.config.os_name.lower()}_init_enable"
start_cmd="{self.config.os_name.lower()}_init_start"

{self.config.os_name.lower()}_init_start()
{{
    echo "Starting {self.config.os_name} initialization..."
    # Add your custom initialization here
}}

load_rc_config $name
run_rc_command "$1"
"""
            custom_rc.write_text(rc_content)
            custom_rc.chmod(0o755)
            self.customizations.append(f"RC script: {custom_rc}")
    
    def _save_customization_log(self):
        """Save log of all customizations"""
        log_file = self.config.work_dir / "customizations.log"
        with open(log_file, 'w') as f:
            f.write(f"{self.config.os_name} Customization Log\n")
            f.write("=" * 50 + "\n\n")
            for item in self.customizations:
                f.write(f"- {item}\n")
        print(f"[i] Customization log: {log_file}")

    def _apply_patches(self):
        """Apply custom patches"""
        from modules.patches import PatchManager
        patch_manager = PatchManager(self.config)
        patch_manager.apply_patches()
    
    def _customize_motd(self):
        """Customize message of the day"""
        if not self.config.custom_motd:
            return
        
        print("[*] Customizing MOTD...")
        motd_path = self.config.src_dir / "etc/motd"
        
        if motd_path.exists():
            motd_path.write_text(self.config.custom_motd)
            self.customizations.append(f"MOTD: {motd_path}")
    
    def _customize_boot_logo(self):
        """Customize boot logo"""
        if not self.config.custom_logo:
            return
        
        print("[*] Customizing boot logo...")
        
        # Create custom logo file
        logo_path = self.config.src_dir / "sys/boot/forth/logo-custom.4th"
        logo_path.parent.mkdir(parents=True, exist_ok=True)
        
        logo_content = f'''\ Custom logo for {self.config.os_name}

: logo ( x y -- )
  2dup at-xy ."  {self.config.os_name} " 1+
  2dup at-xy ." ==================" 1+
  2drop
;
'''
        logo_path.write_text(logo_content)
        
        # Update loader.conf to use custom logo
        loader_conf = self.config.src_dir / "sys/boot/forth/loader.conf"
        if loader_conf.exists():
            content = loader_conf.read_text()
            content += f'\nloader_logo="custom"\n'
            loader_conf.write_text(content)
        
        self.customizations.append(f"Boot logo: {logo_path}")
    
    def _customize_rc_conf(self):
        """Add custom rc.conf settings"""
        if not self.config.custom_rc_conf:
            return
        
        print("[*] Customizing rc.conf...")
        rc_conf_path = self.config.src_dir / "etc/defaults/rc.conf"
        
        if rc_conf_path.exists():
            content = rc_conf_path.read_text()
            content += f"\n# {self.config.os_name} Custom Settings\n"
            
            for key, value in self.config.custom_rc_conf.items():
                content += f'{key}="{value}"\n'
            
            rc_conf_path.write_text(content)
            self.customizations.append(f"rc.conf: {rc_conf_path}")
    
    def _customize_sysctl(self):
        """Add custom sysctl settings"""
        if not self.config.custom_sysctl:
            return
        
        print("[*] Customizing sysctl...")
        sysctl_conf = self.config.src_dir / "etc/sysctl.conf"
        
        content = f"# {self.config.os_name} Custom Sysctl Settings\n"
        for key, value in self.config.custom_sysctl.items():
            content += f"{key}={value}\n"
        
        sysctl_conf.write_text(content)
        self.customizations.append(f"sysctl.conf: {sysctl_conf}")
    
    def _customize_make_conf(self):
        """Customize make.conf"""
        if not self.config.make_conf_additions:
            return
        
        print("[*] Customizing make.conf...")
        make_conf = self.config.src_dir / "etc/make.conf"
        
        content = f"# {self.config.os_name} Custom Make Configuration\n"
        for line in self.config.make_conf_additions:
            content += f"{line}\n"
        
        make_conf.write_text(content)
        self.customizations.append(f"make.conf: {make_conf}")
    
    def _customize_src_conf(self):
        """Customize src.conf"""
        if not self.config.src_conf_additions:
            return
        
        print("[*] Customizing src.conf...")
        src_conf = self.config.src_dir / "etc/src.conf"
        
        content = f"# {self.config.os_name} Custom Source Configuration\n"
        for line in self.config.src_conf_additions:
            content += f"{line}\n"
        
        src_conf.write_text(content)
        self.customizations.append(f"src.conf: {src_conf}")
