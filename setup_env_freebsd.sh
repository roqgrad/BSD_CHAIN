#!/bin/sh
# FreeBSD Custom OS Builder - FreeBSD Development Environment Setup
# This script sets up a complete development environment on FreeBSD

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$SCRIPT_DIR/setup.log"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error() {
    echo "[ERROR] $1" | tee -a "$LOG_FILE"
    exit 1
}

warn() {
    echo "[WARNING] $1" | tee -a "$LOG_FILE"
}

check_root() {
    if [ "$(id -u)" -eq 0 ]; then
        error "Please do not run this script as root. It will use sudo when needed."
    fi
}

install_system_packages() {
    log "Installing system packages..."
    
    sudo pkg update
    sudo pkg install -y \
        git \
        python3 \
        py39-pip \
        py39-virtualenv \
        curl \
        wget \
        vim \
        tmux \
        htop \
        tree \
        jq \
        cdrtools \
        xorriso \
        qemu \
        ccache \
        ninja \
        cmake \
        pkgconf \
        bash \
        gmake \
        || error "Failed to install system packages"
    
    log "System packages installed successfully"
}

install_vscode() {
    log "Installing Visual Studio Code..."
    
    if command -v code >/dev/null 2>&1; then
        log "VS Code already installed"
        return
    fi
    
    # Install VS Code from packages
    sudo pkg install -y vscode || warn "VS Code installation failed, trying alternative method"
    
    # Alternative: Download and install manually
    if ! command -v code >/dev/null 2>&1; then
        log "Installing VS Code manually..."
        cd /tmp
        fetch https://update.code.visualstudio.com/latest/freebsd/stable
        sudo pkg add vscode-*.txz || warn "Manual VS Code installation failed"
        cd "$SCRIPT_DIR"
    fi
    
    log "VS Code installation attempted"
}

install_vscode_extensions() {
    log "Installing VS Code extensions..."
    
    if ! command -v code >/dev/null 2>&1; then
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
    . venv/bin/activate
    
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

setup_freebsd_src() {
    log "Setting up FreeBSD source tree..."
    
    # FreeBSD source is typically in /usr/src
    if [ ! -d "/usr/src/.git" ]; then
        log "FreeBSD source not found in /usr/src"
        log "You can clone it later using the builder"
    else
        log "FreeBSD source found in /usr/src"
    fi
}

setup_git_config() {
    log "Configuring Git..."
    
    # Check if git is already configured
    if git config --global user.name >/dev/null 2>&1; then
        log "Git already configured"
        return
    fi
    
    printf "Enter your Git username: "
    read git_username
    printf "Enter your Git email: "
    read git_email
    
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
    mkdir -p freebsd_workspace/src
    mkdir -p freebsd_workspace/obj
    mkdir -p freebsd_workspace/dist
    mkdir -p freebsd_workspace/ports
    mkdir -p freebsd_workspace/iso
    mkdir -p freebsd_workspace/patches
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
    
    if command -v docker >/dev/null 2>&1; then
        log "Docker already installed"
        return
    fi
    
    # Install Docker on FreeBSD
    sudo pkg install -y docker docker-compose
    
    # Enable Docker service
    sudo sysrc docker_enable="YES"
    sudo service docker start
    
    # Add user to docker group
    sudo pw groupmod docker -m $USER || true
    
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
        },
        "terminal.integrated.shell.freebsd": "/usr/local/bin/bash"
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
export MAKE_JOBS=\$(sysctl -n hw.ncpu)
export CCACHE_DIR="\$HOME/.ccache"

# Python
export PYTHONPATH="$SCRIPT_DIR:\$PYTHONPATH"

# Activate virtual environment
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    . "$SCRIPT_DIR/venv/bin/activate"
fi

# Aliases
alias fbuild='python3 $SCRIPT_DIR/freebsd_builder.py'
alias fclean='python3 $SCRIPT_DIR/freebsd_builder.py --clean'
alias ftest='python3 -m pytest tests/'

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

setup_kernel_build_env() {
    log "Setting up kernel build environment..."
    
    # Add user to wheel group if not already
    sudo pw groupmod wheel -m $USER 2>/dev/null || true
    
    log "Kernel build environment configured"
}

print_summary() {
    echo ""
    echo "=========================================="
    echo "  Setup Complete!"
    echo "=========================================="
    echo ""
    echo "Installed components:"
    echo "  ✓ System packages (git, build tools, etc.)"
    echo "  ✓ Visual Studio Code (if available)"
    echo "  ✓ VS Code extensions"
    echo "  ✓ Python virtual environment"
    echo "  ✓ FreeBSD build tools"
    echo "  ✓ Docker & docker-compose"
    echo "  ✓ Development workspace"
    echo ""
    echo "Next steps:"
    echo "  1. Log out and back in (for group changes)"
    echo "  2. Load environment: . .env"
    echo "  3. Open VS Code: code freebsd-builder.code-workspace"
    echo "  4. Start building: python3 freebsd_builder.py --all"
    echo ""
    echo "Quick commands:"
    echo "  fbuild --all              # Full build"
    echo "  fbuild --create-iso       # Create ISO"
    echo "  gmake all                 # Using Makefile"
    echo ""
    echo "Documentation:"
    echo "  README.md                 # Getting started"
    echo "  ADVANCED_GUIDE.md         # Advanced features"
    echo "  ARCHITECTURE.md           # System design"
    echo ""
}

main() {
    log "Starting FreeBSD Custom OS Builder environment setup for FreeBSD..."
    
    check_root
    install_system_packages
    install_vscode
    install_vscode_extensions
    setup_python_env
    setup_freebsd_src
    setup_git_config
    setup_workspace
    install_docker
    create_vscode_workspace
    create_env_file
    setup_ccache
    setup_kernel_build_env
    
    print_summary
    
    log "Setup completed successfully!"
}

main "$@"
