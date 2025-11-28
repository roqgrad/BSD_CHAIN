#!/bin/bash
# Clean all build artifacts and temporary files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="$SCRIPT_DIR/../freebsd_workspace"

echo "Cleaning FreeBSD Custom OS Builder workspace..."

# Clean build artifacts
if [ -d "$WORKSPACE/obj" ]; then
    echo "Removing obj directory..."
    rm -rf "$WORKSPACE/obj"
fi

if [ -d "$WORKSPACE/dist" ]; then
    echo "Removing dist directory..."
    rm -rf "$WORKSPACE/dist"
fi

if [ -d "$WORKSPACE/iso" ]; then
    echo "Removing iso directory..."
    rm -rf "$WORKSPACE/iso"
fi

# Clean Python cache
echo "Cleaning Python cache..."
find "$SCRIPT_DIR/.." -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$SCRIPT_DIR/.." -type f -name "*.pyc" -delete 2>/dev/null || true

# Clean logs
if [ -d "$SCRIPT_DIR/../logs" ]; then
    echo "Cleaning logs..."
    rm -f "$SCRIPT_DIR/../logs"/*.log
fi

echo "✓ Cleanup complete!"
echo ""
echo "Note: Source code in $WORKSPACE/src was preserved"
echo "To remove source: rm -rf $WORKSPACE/src"
