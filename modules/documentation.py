"""Documentation generation module"""

from pathlib import Path
from datetime import datetime

class DocumentationGenerator:
    """Generates documentation for the custom OS"""
    
    def __init__(self, config):
        self.config = config
        self.docs_dir = config.work_dir / "docs"
        self.docs_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_all(self):
        """Generate all documentation"""
        print("[*] Generating documentation...")
        
        self._generate_build_info()
        self._generate_package_list()
        self._generate_kernel_config_doc()
        self._generate_changelog()
        
        print(f"[✓] Documentation generated in {self.docs_dir}")
    
    def _generate_build_info(self):
        """Generate build information document"""
        doc_file = self.docs_dir / "BUILD_INFO.md"
        
        content = f"""# {self.config.os_name} Build Information

## Build Details
- **OS Name**: {self.config.os_name}
- **Version**: {self.config.version}
- **Architecture**: {self.config.target_arch}
- **Build Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Configuration
- **Kernel Config**: {self.config.custom_kernel_config or self.config.kernel_config}
- **Make Jobs**: {self.config.make_jobs}
- **Source Branch**: {self.config.git_branch}

## Features
"""
        
        if hasattr(self.config, 'kernel_options') and self.config.kernel_options:
            content += "\n### Kernel Options\n"
            for opt in self.config.kernel_options:
                content += f"- {opt}\n"
        
        if hasattr(self.config, 'custom_packages') and self.config.custom_packages:
            content += "\n### Custom Packages\n"
            for pkg in self.config.custom_packages:
                content += f"- {pkg}\n"
        
        doc_file.write_text(content)
    
    def _generate_package_list(self):
        """Generate package list"""
        doc_file = self.docs_dir / "PACKAGES.md"
        
        content = f"""# {self.config.os_name} Package List

## Base System Packages
The following packages are included in the base system:

"""
        
        if hasattr(self.config, 'custom_packages') and self.config.custom_packages:
            for pkg in self.config.custom_packages:
                content += f"- **{pkg}**\n"
        else:
            content += "No custom packages configured.\n"
        
        doc_file.write_text(content)
    
    def _generate_kernel_config_doc(self):
        """Generate kernel configuration documentation"""
        doc_file = self.docs_dir / "KERNEL_CONFIG.md"
        
        content = f"""# {self.config.os_name} Kernel Configuration

## Base Configuration
Based on: {self.config.kernel_config}

## Custom Options
"""
        
        if hasattr(self.config, 'kernel_options') and self.config.kernel_options:
            for opt in self.config.kernel_options:
                content += f"- `{opt}`\n"
        
        if hasattr(self.config, 'kernel_devices') and self.config.kernel_devices:
            content += "\n## Additional Devices\n"
            for dev in self.config.kernel_devices:
                content += f"- `{dev}`\n"
        
        if hasattr(self.config, 'kernel_nodevices') and self.config.kernel_nodevices:
            content += "\n## Removed Devices\n"
            for dev in self.config.kernel_nodevices:
                content += f"- `{dev}`\n"
        
        doc_file.write_text(content)
    
    def _generate_changelog(self):
        """Generate changelog"""
        doc_file = self.docs_dir / "CHANGELOG.md"
        
        content = f"""# {self.config.os_name} Changelog

## Version {self.config.version} - {datetime.now().strftime("%Y-%m-%d")}

### Added
- Initial release based on FreeBSD {self.config.version}
- Custom branding and configuration

### Changed
- Modified kernel configuration
- Updated system defaults

### Security
- Applied security hardening
- Configured firewall defaults
"""
        
        doc_file.write_text(content)
