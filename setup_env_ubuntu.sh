#!/bin/bash
# FreeBSD Custom OS Builder - Ubuntu Development Environment Setup
# This script sets up a complete development environment on Ubuntu

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/setup.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

check_root() {
    if [ "$EUID" -eq 0 ]; then
        error "Please do not run this script as root. It will use sudo when needed."
    fi
}

install_system_packages() {
    log "Installing system packages..."
    
    sudo apt-get update
    sudo apt-get install -y \
        git \
        build-essential \
        python3 \
        python3-pip \
        python3-venv \
        curl \
        wget \
        vim \
        tmux \
        htop \
        tree \
        jq \
        xorriso \
        genisoimage \
        qemu-system-x86 \
        qemu-utils \
        libncurses5-dev \
        libssl-dev \
        bc \
        flex \
        bison \
        ccache \
        ninja-build \
        cmake \
        pkg-config \
        || error "Failed to install system packages"
    
    log "System packages installed successfully"
}

install_vscode() {
    log "Installing Visual Studio Code..."
    
    if command -v code &> /dev/null; then
        log "VS Code already installed"
        return
    fi
    
    # Download and install VS Code
    wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
    sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
    sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
    rm -f packages.microsoft.gpg
    
    sudo apt-get update
    sudo apt-get install -y code || error "Failed to install VS Code"
    
    log "VS Code installed successfully"
}

install_vscode_extensions() {
    log "Installing VS Code extensions..."
    
    if ! command -v code &> /dev/null; then
        warn "VS Code not found, skipping extensions"
        return
    fi
    
    # Python extensions
    code --install-extension ms-python.python
    code --install-extension ms-python.vscode-pylance
    
    # Git extensions
    code --install-extension eamodio.gitlens
    code --install-extension mhutchie.git-graph
    
    # Utilities
    code --install-extension streetsidesoftware.code-spell-checker
    code --install-extension editorconfig.editorconfig
    code --install-extension ms-vscode.makefile-tools
    
    # Docker
    code --install-extension ms-azuretools.vscode-docker
    
    # JSON/YAML
    code --install-extension redhat.vscode-yaml
    
    log "VS Code extensions installed"
}

setup_python_env() {
    log "Setting up Python virtual environment..."
    
    cd "$SCRIPT_DIR"
    
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    # Install Python packages
    pip install \
        pytest \
        pytest-cov \
        black \
        flake8 \
        pylint \
        mypy \
        ipython \
        requests \
        pyyaml \
        || error "Failed to install Python packages"
    
    log "Python environment setup complete"
}

install_freebsd_tools() {
    log "Installing FreeBSD build tools..."
    
    # Install cross-compilation tools if needed
    sudo apt-get install -y \
        gcc-aarch64-linux-gnu \
        gcc-riscv64-linux-gnu \
        || warn "Some cross-compilation tools failed to install"
    
    log "FreeBSD tools installed"
}

setup_git_config() {
    log "Configuring Git..."
    
    # Check if git is already configured
    if git config --global user.name &> /dev/null; then
        log "Git already configured"
        return
    fi
    
    read -p "Enter your Git username: " git_username
    read -p "Enter your Git email: " git_email
    
    git config --global user.name "$git_username"
    git config --global user.email "$git_email"
    git config --global core.editor "vim"
    git config --global init.defaultBranch main
    
    log "Git configured successfully"
}

setup_workspace() {
    log "Setting up workspace..."
    
    cd "$SCRIPT_DIR"
    
    # Create necessary directories
    mkdir -p freebsd_workspace/{src,obj,dist,ports,iso,patches}
    mkdir -p logs
    mkdir -p backups
    
    # Set permissions
    chmod +x scripts/*.sh 2>/dev/null || true
    chmod +x scripts/*.py 2>/dev/null || true
    chmod +x hooks/*.sh 2>/dev/null || true
    
    log "Workspace setup complete"
}

install_docker() {
    log "Installing Docker..."
    
    if command -v docker &> /dev/null; then
        log "Docker already installed"
        return
    fi
    
    # Install Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    rm get-docker.sh
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    
    # Install docker-compose
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    log "Docker installed successfully"
    warn "You need to log out and back in for Docker group changes to take effect"
}

create_vscode_workspace() {
    log "Creating VS Code workspace..."
    
    cat > "$SCRIPT_DIR/freebsd-builder.code-workspace" << 'EOF'
{
    "folders": [
        {
            "path": "."
        }
    ],
    "settings": {
        "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
        "python.linting.flake8Enabled": true,
        "python.formatting.provider": "black",
        "editor.formatOnSave": true,
        "files.exclude": {
            "**/__pycache__": true,
            "**/*.pyc": true,
            "freebsd_workspace/src": true,
            "freebsd_workspace/obj": true
        },
        "files.watcherExclude": {
            "**/freebsd_workspace/**": true
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
EOF
    
    log "VS Code workspace created"
}

create_env_file() {
    log "Creating environment file..."
    
    cat > "$SCRIPT_DIR/.env" << EOF
# FreeBSD Custom OS Builder Environment Variables

# Workspace
export FREEBSD_WORKSPACE="$SCRIPT_DIR/freebsd_workspace"
export FREEBSD_SRC="\$FREEBSD_WORKSPACE/src"
export FREEBSD_OBJ="\$FREEBSD_WORKSPACE/obj"
export FREEBSD_DIST="\$FREEBSD_WORKSPACE/dist"

# Build settings
export MAKE_JOBS=$(nproc)
export CCACHE_DIR="\$HOME/.ccache"

# Python
export PYTHONPATH="$SCRIPT_DIR:\$PYTHONPATH"

# Activate virtual environment
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# Aliases
alias fbuild='python $SCRIPT_DIR/freebsd_builder.py'
alias fclean='python $SCRIPT_DIR/freebsd_builder.py --clean'
alias ftest='python -m pytest tests/'

echo "FreeBSD Builder environment loaded"
echo "Workspace: \$FREEBSD_WORKSPACE"
echo "Jobs: \$MAKE_JOBS"
EOF
    
    log "Environment file created at .env"
}

setup_ccache() {
    log "Setting up ccache..."
    
    mkdir -p ~/.ccache
    
    cat > ~/.ccache/ccache.conf << EOF
max_size = 10.0G
compression = true
compression_level = 6
EOF
    
    log "ccache configured"
}

print_summary() {
    echo ""
    echo "=========================================="
    echo "  Setup Complete!"
    echo "=========================================="
    echo ""
    echo "Installed components:"
    echo "  ✓ System packages (git, build tools, etc.)"
    echo "  ✓ Visual Studio Code"
    echo "  ✓ VS Code extensions"
    echo "  ✓ Python virtual environment"
    echo "  ✓ FreeBSD build tools"
    echo "  ✓ Docker & docker-compose"
    echo "  ✓ Development workspace"
    echo ""
    echo "Next steps:"
    echo "  1. Log out and back in (for Docker group)"
    echo "  2. Load environment: source .env"
    echo "  3. Open VS Code: code freebsd-builder.code-workspace"
    echo "  4. Start building: python freebsd_builder.py --all"
    echo ""
    echo "Quick commands:"
    echo "  fbuild --all              # Full build"
    echo "  fbuild --create-iso       # Create ISO"
    echo "  make all                  # Using Makefile"
    echo ""
    echo "Documentation:"
    echo "  README.md                 # Getting started"
    echo "  ADVANCED_GUIDE.md         # Advanced features"
    echo "  ARCHITECTURE.md           # System design"
    echo ""
}

main() {
    log "Starting FreeBSD Custom OS Builder environment setup for Ubuntu..."
    
    check_root
    install_system_packages
    install_vscode
    install_vscode_extensions
    setup_python_env
    install_freebsd_tools
    setup_git_config
    setup_workspace
    install_docker
    create_vscode_workspace
    create_env_file
    setup_ccache
    
    print_summary
    
    log "Setup completed successfully!"
}

main "$@"
