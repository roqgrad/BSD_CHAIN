#!/usr/bin/env python3
"""
Check if all required dependencies are installed
"""

import sys
import shutil
import subprocess
from pathlib import Path

class DependencyChecker:
    """Check system dependencies"""
    
    def __init__(self):
        self.missing = []
        self.installed = []
    
    def check_command(self, cmd, name=None):
        """Check if command exists"""
        name = name or cmd
        if shutil.which(cmd):
            self.installed.append(name)
            return True
        else:
            self.missing.append(name)
            return False
    
    def check_python_module(self, module):
        """Check if Python module is installed"""
        try:
            __import__(module)
            self.installed.append(f"Python: {module}")
            return True
        except ImportError:
            self.missing.append(f"Python: {module}")
            return False
    
    def check_file(self, filepath, name):
        """Check if file exists"""
        if Path(filepath).exists():
            self.installed.append(name)
            return True
        else:
            self.missing.append(name)
            return False
    
    def check_all(self):
        """Check all dependencies"""
        print("Checking dependencies...\n")
        
        # Core tools
        print("Core Tools:")
        self.check_command('git', 'Git')
        self.check_command('python3', 'Python 3')
        self.check_command('make', 'Make')
        self.check_command('gcc', 'GCC')
        
        # Build tools
        print("\nBuild Tools:")
        self.check_command('ccache', 'ccache')
        self.check_command('cmake', 'CMake')
        self.check_command('ninja', 'Ninja')
        
        # ISO tools
        print("\nISO Tools:")
        self.check_command('mkisofs', 'mkisofs')
        self.check_command('xorriso', 'xorriso')
        
        # Virtualization
        print("\nVirtualization:")
        self.check_command('qemu-system-x86_64', 'QEMU')
        self.check_command('docker', 'Docker')
        
        # Development tools
        print("\nDevelopment Tools:")
        self.check_command('code', 'VS Code')
        self.check_command('vim', 'Vim')
        self.check_command('tmux', 'tmux')
        
        # Python modules
        print("\nPython Modules:")
        self.check_python_module('pytest')
        self.check_python_module('black')
        self.check_python_module('flake8')
        
        # Project files
        print("\nProject Files:")
        self.check_file('freebsd_builder.py', 'Main builder script')
        self.check_file('modules/config.py', 'Config module')
        self.check_file('requirements.txt', 'Requirements file')
        
        # Virtual environment
        self.check_file('venv/bin/python', 'Python virtual environment')
    
    def print_report(self):
        """Print dependency report"""
        print("\n" + "=" * 60)
        print("Dependency Check Report")
        print("=" * 60)
        
        print(f"\n✓ Installed: {len(self.installed)}")
        for item in self.installed:
            print(f"  ✓ {item}")
        
        if self.missing:
            print(f"\n✗ Missing: {len(self.missing)}")
            for item in self.missing:
                print(f"  ✗ {item}")
            
            print("\nTo install missing dependencies, run:")
            print("  python3 setup_dev_env.py")
            return False
        else:
            print("\n✓ All dependencies are installed!")
            return True

def main():
    """Main entry point"""
    checker = DependencyChecker()
    checker.check_all()
    
    if checker.print_report():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
