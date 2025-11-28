#!/bin/sh
# Pre-build hook example
# This script runs before the build starts

echo "[HOOK] Pre-build hook executing..."
echo "[HOOK] OS Name: $OS_NAME"
echo "[HOOK] Version: $OS_VERSION"
echo "[HOOK] Source: $FREEBSD_SRC"

# Example: Check disk space
df -h "$FREEBSD_OBJ"

# Example: Backup previous build
if [ -d "$FREEBSD_DIST" ]; then
    echo "[HOOK] Backing up previous distribution..."
    tar -czf "$FREEBSD_DIST.backup.tar.gz" "$FREEBSD_DIST" 2>/dev/null || true
fi

echo "[HOOK] Pre-build hook completed"
