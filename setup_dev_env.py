#!/usr/bin/env python3
"""
FreeBSD Custom OS Builder - Development Environment Setup
Cross-platform setup script for Ubuntu and FreeBSD
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import json

class Colors:
    """ANSI color codes"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

class DevEnvSetup:
    """Development environment setup manager"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent.resolve()
        self.log_file = self.script_dir / "setup.log"
        self.os_type = self._detect_os()
        self.is_root = os.geteuid() == 0 if hasattr(os, 'geteuid') else False
    
    def _detect_os(self):
        """Detect operating system"""
        system = platform.system().lower()
        if system == 'linux':
            # Check if it's Ubuntu
            try:
                with open('/etc/os-release') as f:
                    if 'ubuntu' in f.read().lower():
                        return 'ubuntu'
            except:
                pass
            return 'linux'
        elif system == 'freebsd':
            return 'freebsd'
        else:
            return system
    
    def log(self, message):
        """Log message to console and file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {message}"
        print(f"{Colors.GREEN}{log_msg}{Colors.NC}")
        
        with open(self.log_file, 'a') as f:
            f.write(log_msg + '\n')
    
    def error(self, message):
        """Log error and exit"""
        print(f"{Colors.RED}[ERROR] {message}{Colors.NC}")
        with open(self.log_file, 'a') as f:
            f.write(f"[ERROR] {message}\n")
        sys.exit(1)
    
    def warn(self, message):
        """Log warning"""
        print(f"{Colors.YELLOW}[WARNING] {message}{Colors.NC}")
        with open(self.log_file, 'a') as f:
            f.write(f"[WARNING] {message}\n")
    
    def run_command(self, cmd, check=True, shell=False):
        """Run shell command"""
        try:
            if isinstance(cmd, str) and not shell:
                cmd = cmd.split()
            
            result = subprocess.run(
                cmd,
                check=check,
                capture_output=True,
                text=True,
                shell=shell
            )
            return result
        except subprocess.CalledProcessError as e:
            if check:
                self.error(f"Command failed: {cmd}\n{e.stderr}")
            return None
    
    def check_root(self):
        """Check if running as root"""
        if self.is_root:
            self.error("Please do not run this script as root. It will use sudo when needed.")
    
    def install_system_packages(self):
        """Install system packages based on OS"""
        self.log("Installing system packages...")
        
        if self.os_type == 'ubuntu':
            self._install_ubuntu_packages()
        elif self.os_type == 'freebsd':
            self._install_freebsd_packages()
        else:
            self.warn(f"Unsupported OS: {self.os_type}")
    
    def _install_ubuntu_packages(self):
        """Install Ubuntu packages"""
        packages = [
            'git', 'build-essential', 'python3', 'python3-pip', 'python3-venv',
            'curl', 'wget', 'vim', 'tmux', 'htop', 'tree', 'jq',
            'xorriso', 'genisoimage', 'qemu-system-x86', 'qemu-utils',
            'libncurses5-dev', 'libssl-dev', 'bc', 'flex', 'bison',
            'ccache', 'ninja-build', 'cmake', 'pkg-config'
        ]
        
        self.run_command(['sudo', 'apt-get', 'update'])
        self.run_command(['sudo', 'apt-get', 'install', '-y'] + packages)
        self.log("Ubuntu packages installed successfully")
    
    def _install_freebsd_packages(self):
        """Install FreeBSD packages"""
        packages = [
            'git', 'python3', 'py39-pip', 'py39-virtualenv',
            'curl', 'wget', 'vim', 'tmux', 'htop', 'tree', 'jq',
            'cdrtools', 'xorriso', 'qemu', 'ccache', 'ninja',
            'cmake', 'pkgconf', 'bash', 'gmake'
        ]
        
        self.run_command(['sudo', 'pkg', 'update'])
        self.run_command(['sudo', 'pkg', 'install', '-y'] + packages)
        self.log("FreeBSD packages installed successfully")
    
    def install_vscode(self):
        """Install Visual Studio Code"""
        self.log("Installing Visual Studio Code...")
        
        if shutil.which('code'):
            self.log("VS Code already installed")
            return
        
        if self.os_type == 'ubuntu':
            self._install_vscode_ubuntu()
        elif self.os_type == 'freebsd':
            self._install_vscode_freebsd()
    
    def _install_vscode_ubuntu(self):
        """Install VS Code on Ubuntu"""
        # Download Microsoft GPG key
        self.run_command(
            'wget -qO- https://packages.microsoft.com/keys/microsoft.asc | '
            'gpg --dearmor > packages.microsoft.gpg',
            shell=True
        )
        
        self.run_command([
            'sudo', 'install', '-o', 'root', '-g', 'root', '-m', '644',
            'packages.microsoft.gpg', '/etc/apt/trusted.gpg.d/'
        ])
        
        # Add repository
        repo_line = 'deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] ' \
                   'https://packages.microsoft.com/repos/code stable main'
        
        self.run_command(
            f'echo "{repo_line}" | sudo tee /etc/apt/sources.list.d/vscode.list',
            shell=True
        )
        
        # Clean up
        Path('packages.microsoft.gpg').unlink(missing_ok=True)
        
        # Install
        self.run_command(['sudo', 'apt-get', 'update'])
        self.run_command(['sudo', 'apt-get', 'install', '-y', 'code'])
        self.log("VS Code installed successfully")
    
    def _install_vscode_freebsd(self):
        """Install VS Code on FreeBSD"""
        result = self.run_command(['sudo', 'pkg', 'install', '-y', 'vscode'], check=False)
        if result and result.returncode == 0:
            self.log("VS Code installed successfully")
        else:
            self.warn("VS Code installation failed on FreeBSD")
    
    def install_vscode_extensions(self):
        """Install VS Code extensions"""
        self.log("Installing VS Code extensions...")
        
        if not shutil.which('code'):
            self.warn("VS Code not found, skipping extensions")
            return
        
        extensions = [
            'ms-python.python',
            'ms-python.vscode-pylance',
            'eamodio.gitlens',
            'mhutchie.git-graph',
            'streetsidesoftware.code-spell-checker',
            'editorconfig.editorconfig',
            'ms-vscode.makefile-tools',
            'ms-azuretools.vscode-docker',
            'redhat.vscode-yaml',
        ]
        
        for ext in extensions:
            self.run_command(['code', '--install-extension', ext], check=False)
        
        self.log("VS Code extensions installed")
    
    def setup_python_env(self):
        """Setup Python virtual environment"""
        self.log("Setting up Python virtual environment...")
        
        venv_dir = self.script_dir / 'venv'
        
        # Create virtual environment
        self.run_command([sys.executable, '-m', 'venv', str(venv_dir)])
        
        # Determine pip path
        if self.os_type == 'freebsd':
            pip_path = venv_dir / 'bin' / 'pip'
        else:
            pip_path = venv_dir / 'bin' / 'pip'
        
        # Upgrade pip
        self.run_command([str(pip_path), 'install', '--upgrade', 'pip', 'setuptools', 'wheel'])
        
        # Install requirements
        requirements_file = self.script_dir / 'requirements.txt'
        if requirements_file.exists():
            self.run_command([str(pip_path), 'install', '-r', str(requirements_file)])
        
        self.log("Python environment setup complete")
    
    def setup_git_config(self):
        """Configure Git"""
        self.log("Configuring Git...")
        
        # Check if already configured
        result = self.run_command(['git', 'config', '--global', 'user.name'], check=False)
        if result and result.returncode == 0 and result.stdout.strip():
            self.log("Git already configured")
            return
        
        print("\nGit Configuration:")
        git_username = input("Enter your Git username: ").strip()
        git_email = input("Enter your Git email: ").strip()
        
        if git_username:
            self.run_command(['git', 'config', '--global', 'user.name', git_username])
        if git_email:
            self.run_command(['git', 'config', '--global', 'user.email', git_email])
        
        self.run_command(['git', 'config', '--global', 'core.editor', 'vim'])
        self.run_command(['git', 'config', '--global', 'init.defaultBranch', 'main'])
        
        self.log("Git configured successfully")
    
    def setup_workspace(self):
        """Setup workspace directories"""
        self.log("Setting up workspace...")
        
        directories = [
            'freebsd_workspace/src',
            'freebsd_workspace/obj',
            'freebsd_workspace/dist',
            'freebsd_workspace/ports',
            'freebsd_workspace/iso',
            'freebsd_workspace/patches',
            'logs',
            'backups',
        ]
        
        for dir_path in directories:
            (self.script_dir / dir_path).mkdir(parents=True, exist_ok=True)
        
        # Set permissions for scripts
        for script_dir in ['scripts', 'hooks']:
            script_path = self.script_dir / script_dir
            if script_path.exists():
                for script_file in script_path.glob('*'):
                    if script_file.is_file():
                        script_file.chmod(0o755)
        
        self.log("Workspace setup complete")
    
    def install_docker(self):
        """Install Docker"""
        self.log("Installing Docker...")
        
        if shutil.which('docker'):
            self.log("Docker already installed")
            return
        
        if self.os_type == 'ubuntu':
            self._install_docker_ubuntu()
        elif self.os_type == 'freebsd':
            self._install_docker_freebsd()
    
    def _install_docker_ubuntu(self):
        """Install Docker on Ubuntu"""
        # Download and run Docker install script
        self.run_command('curl -fsSL https://get.docker.com -o get-docker.sh', shell=True)
        self.run_command(['sudo', 'sh', 'get-docker.sh'])
        Path('get-docker.sh').unlink(missing_ok=True)
        
        # Add user to docker group
        username = os.getenv('USER')
        if username:
            self.run_command(['sudo', 'usermod', '-aG', 'docker', username])
        
        # Install docker-compose
        compose_url = 'https://github.com/docker/compose/releases/latest/download/docker-compose-Linux-x86_64'
        self.run_command(f'sudo curl -L "{compose_url}" -o /usr/local/bin/docker-compose', shell=True)
        self.run_command(['sudo', 'chmod', '+x', '/usr/local/bin/docker-compose'])
        
        self.log("Docker installed successfully")
        self.warn("You need to log out and back in for Docker group changes to take effect")
    
    def _install_docker_freebsd(self):
        """Install Docker on FreeBSD"""
        self.run_command(['sudo', 'pkg', 'install', '-y', 'docker', 'docker-compose'])
        self.run_command(['sudo', 'sysrc', 'docker_enable=YES'])
        self.run_command(['sudo', 'service', 'docker', 'start'], check=False)
        
        username = os.getenv('USER')
        if username:
            self.run_command(['sudo', 'pw', 'groupmod', 'docker', '-m', username], check=False)
        
        self.log("Docker installed successfully")
    
    def create_vscode_workspace(self):
        """Create VS Code workspace file"""
        self.log("Creating VS Code workspace...")
        
        workspace_config = {
            "folders": [{"path": "."}],
            "settings": {
                "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
                "python.linting.enabled": True,
                "python.linting.pylintEnabled": True,
                "python.linting.flake8Enabled": True,
                "python.formatting.provider": "black",
                "editor.formatOnSave": True,
                "files.exclude": {
                    "**/__pycache__": True,
                    "**/*.pyc": True,
                    "freebsd_workspace/src": True,
                    "freebsd_workspace/obj": True
                },
                "files.watcherExclude": {
                    "**/freebsd_workspace/**": True
                }
            },
            "extensions": {
                "recommendations": [
                    "ms-python.python",
                    "ms-python.vscode-pylance",
                    "eamodio.gitlens",
                    "ms-azuretools.vscode-docker"
                ]
            }
        }
        
        workspace_file = self.script_dir / 'freebsd-builder.code-workspace'
        with open(workspace_file, 'w') as f:
            json.dump(workspace_config, f, indent=4)
        
        self.log("VS Code workspace created")
    
    def create_env_file(self):
        """Create environment file"""
        self.log("Creating environment file...")
        
        # Detect number of CPU cores
        try:
            if self.os_type == 'freebsd':
                result = self.run_command(['sysctl', '-n', 'hw.ncpu'])
                cpu_count = result.stdout.strip()
            else:
                cpu_count = str(os.cpu_count() or 4)
        except:
            cpu_count = '4'
        
        env_content = f"""# FreeBSD Custom OS Builder Environment Variables

# Workspace
export FREEBSD_WORKSPACE="{self.script_dir}/freebsd_workspace"
export FREEBSD_SRC="$FREEBSD_WORKSPACE/src"
export FREEBSD_OBJ="$FREEBSD_WORKSPACE/obj"
export FREEBSD_DIST="$FREEBSD_WORKSPACE/dist"

# Build settings
export MAKE_JOBS={cpu_count}
export CCACHE_DIR="$HOME/.ccache"

# Python
export PYTHONPATH="{self.script_dir}:$PYTHONPATH"

# Activate virtual environment
if [ -f "{self.script_dir}/venv/bin/activate" ]; then
    source "{self.script_dir}/venv/bin/activate"
fi

# Aliases
alias fbuild='python3 {self.script_dir}/freebsd_builder.py'
alias fclean='python3 {self.script_dir}/freebsd_builder.py --clean'
alias ftest='python3 -m pytest tests/'

echo "FreeBSD Builder environment loaded"
echo "Workspace: $FREEBSD_WORKSPACE"
echo "Jobs: $MAKE_JOBS"
"""
        
        env_file = self.script_dir / '.env'
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        self.log("Environment file created at .env")
    
    def setup_ccache(self):
        """Setup ccache"""
        self.log("Setting up ccache...")
        
        ccache_dir = Path.home() / '.ccache'
        ccache_dir.mkdir(parents=True, exist_ok=True)
        
        ccache_config = """max_size = 10.0G
compression = true
compression_level = 6
"""
        
        config_file = ccache_dir / 'ccache.conf'
        with open(config_file, 'w') as f:
            f.write(ccache_config)
        
        self.log("ccache configured")
    
    def print_summary(self):
        """Print setup summary"""
        print("\n" + "=" * 60)
        print("  Setup Complete!")
        print("=" * 60)
        print("\nInstalled components:")
        print("  ✓ System packages (git, build tools, etc.)")
        print("  ✓ Visual Studio Code")
        print("  ✓ VS Code extensions")
        print("  ✓ Python virtual environment")
        print("  ✓ FreeBSD build tools")
        print("  ✓ Docker & docker-compose")
        print("  ✓ Development workspace")
        print("\nNext steps:")
        print("  1. Log out and back in (for Docker group)")
        print("  2. Load environment: source .env")
        print("  3. Open VS Code: code freebsd-builder.code-workspace")
        print("  4. Start building: python3 freebsd_builder.py --all")
        print("\nQuick commands:")
        print("  fbuild --all              # Full build")
        print("  fbuild --create-iso       # Create ISO")
        print("  make all                  # Using Makefile")
        print("\nDocumentation:")
        print("  README.md                 # Getting started")
        print("  ADVANCED_GUIDE.md         # Advanced features")
        print("  ARCHITECTURE.md           # System design")
        print()
    
    def run_setup(self):
        """Run complete setup"""
        self.log(f"Starting FreeBSD Custom OS Builder environment setup for {self.os_type}...")
        
        self.check_root()
        self.install_system_packages()
        self.install_vscode()
        self.install_vscode_extensions()
        self.setup_python_env()
        self.setup_git_config()
        self.setup_workspace()
        self.install_docker()
        self.create_vscode_workspace()
        self.create_env_file()
        self.setup_ccache()
        
        self.print_summary()
        self.log("Setup completed successfully!")

def main():
    """Main entry point"""
    print(f"{Colors.BLUE}")
    print("=" * 60)
    print("  FreeBSD Custom OS Builder")
    print("  Development Environment Setup")
    print("=" * 60)
    print(f"{Colors.NC}\n")
    
    setup = DevEnvSetup()
    
    try:
        setup.run_setup()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup interrupted by user{Colors.NC}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}Setup failed: {e}{Colors.NC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main