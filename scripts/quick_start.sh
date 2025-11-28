#!/bin/bash
# Quick start script for FreeBSD Custom OS Builder

set -e

echo "FreeBSD Custom OS Builder - Quick Start"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required"
    exit 1
fi

# Check Git
if ! command -v git &> /dev/null; then
    echo "Error: Git is required"
    exit 1
fi

# Get user input
read -p "Enter your OS name [CustomBSD]: " OS_NAME
OS_NAME=${OS_NAME:-CustomBSD}

read -p "Enter FreeBSD version [14.0-RELEASE]: " VERSION
VERSION=${VERSION:-14.0-RELEASE}

read -p "Enter target architecture [amd64]: " ARCH
ARCH=${ARCH:-amd64}

read -p "Number of parallel jobs [4]: " JOBS
JOBS=${JOBS:-4}

read -p "Create ISO image? (y/n) [n]: " CREATE_ISO
CREATE_ISO=${CREATE_ISO:-n}

# Build command
CMD="python3 freebsd_builder.py --all --os-name \"$OS_NAME\" --version \"$VERSION\" --target \"$ARCH\" --jobs $JOBS"

if [ "$CREATE_ISO" = "y" ]; then
    CMD="$CMD --create-iso"
fi

echo ""
echo "Configuration:"
echo "  OS Name: $OS_NAME"
echo "  Version: $VERSION"
echo "  Architecture: $ARCH"
echo "  Jobs: $JOBS"
echo "  Create ISO: $CREATE_ISO"
echo ""
echo "Command: $CMD"
echo ""

read -p "Start build? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    echo "Aborted"
    exit 0
fi

echo ""
echo "Starting build..."
eval $CMD

echo ""
echo "Build complete!"
