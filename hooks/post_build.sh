#!/bin/sh
# Post-build hook example
# This script runs after the build completes

echo "[HOOK] Post-build hook executing..."

# Example: Generate checksums
if [ -d "$FREEBSD_DIST" ]; then
    echo "[HOOK] Generating checksums..."
    cd "$FREEBSD_DIST"
    find . -type f -exec sha256sum {} \; > ../checksums.txt
    echo "[HOOK] Checksums saved to checksums.txt"
fi

# Example: Create build report
cat > "$FREEBSD_OBJ/../build_report.txt" << EOF
Build Report for $OS_NAME
========================
Version: $OS_VERSION
Build Date: $(date)
Source: $FREEBSD_SRC
Distribution: $FREEBSD_DIST

Build completed successfully!
EOF

echo "[HOOK] Post-build hook completed"
