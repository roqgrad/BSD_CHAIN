# Advanced FreeBSD Custom OS Builder Guide

## Table of Contents
1. [Advanced Configuration](#advanced-configuration)
2. [Kernel Customization](#kernel-customization)
3. [Patch Management](#patch-management)
4. [Package Integration](#package-integration)
5. [ISO Creation](#iso-creation)
6. [Cross-Compilation](#cross-compilation)
7. [Build Hooks](#build-hooks)
8. [Testing & Validation](#testing--validation)

## Advanced Configuration

### Complete Configuration File

```json
{
  "work_dir": "./freebsd_workspace",
  "os_name": "MyCustomOS",
  "version": "14.0-RELEASE",
  "target_arch": "amd64",
  "make_jobs": 8,
  
  "kernel_options": ["ALTQ", "IPSEC"],
  "kernel_devices": ["pf", "pflog"],
  "kernel_nodevices": ["fdc"],
  
  "custom_packages": ["bash", "vim", "git"],
  "custom_rc_conf": {
    "hostname": "mycustomos",
    "sshd_enable": "YES"
  },
  
  "create_iso": true,
  "pre_build_hooks": ["./hooks/pre_build.sh"],
  "post_build_hooks": ["./hooks/post_build.sh"]
}
```

## Kernel Customization

### Adding Kernel Options

```python
config.kernel_options = [
    "ALTQ",              # Traffic shaping
    "IPSEC",             # IPsec support
    "IPSEC_SUPPORT",     # IPsec kernel support
    "NETGRAPH",          # Netgraph networking
    "VIMAGE",            # Network stack virtualization
]
```

### Custom Devices

```python
config.kernel_devices = [
    "pf",                # Packet filter
    "pflog",             # PF logging
    "carp",              # Common Address Redundancy Protocol
]

config.kernel_nodevices = [
    "fdc",               # Floppy disk controller
    "uart",              # Serial ports (if not needed)
]
```

## Patch Management

### Creating Patches

```bash
# Method 1: Manual diff
cd freebsd_workspace/src
# Make your changes
git diff > ../patches/001-my-feature.patch

# Method 2: Using the toolchain
python -c "
from modules.patches import PatchManager
from modules.config import Config
config = Config('./freebsd_workspace', 'MyOS', '14.0-RELEASE', 'amd64')
pm = PatchManager(config)
pm.create_patch('security_hardening', ['sys/kern/kern_exec.c'])
"
```

### Patch Structure

```patch
--- a/sys/kern/kern_exec.c
+++ b/sys/kern/kern_exec.c
@@ -100,6 +100,7 @@
 #include <sys/proc.h>
+#include <sys/custom.h>
```

## Package Integration

### Building Custom Packages

```bash
# Setup ports and build packages
python freebsd_builder.py --setup-ports --build-packages --config advanced_config.json
```

### Package Configuration

```json
{
  "enable_ports": true,
  "custom_packages": [
    "shells/bash",
    "editors/vim",
    "devel/git",
    "security/sudo"
  ]
}
```

## ISO Creation

### Creating Bootable ISO

```bash
# Build everything and create ISO
python freebsd_builder.py --all --create-iso

# Just create ISO from existing build
python freebsd_builder.py --create-iso
```

### USB Memstick Image

```bash
python freebsd_builder.py --create-memstick
```

## Cross-Compilation

### ARM64 Build

```bash
python freebsd_builder.py --all \
  --target arm64 \
  --cross-compile aarch64-freebsd \
  --os-name "MyOS-ARM"
```

### RISC-V Build

```bash
python freebsd_builder.py --all \
  --target riscv64 \
  --cross-compile riscv64-freebsd \
  --os-name "MyOS-RISCV"
```

## Build Hooks

### Pre-Build Hook Example

```bash
#!/bin/sh
# hooks/pre_build.sh

echo "Checking build environment..."
df -h "$FREEBSD_OBJ"

# Backup previous build
if [ -d "$FREEBSD_DIST" ]; then
    tar -czf "$FREEBSD_DIST.backup.tar.gz" "$FREEBSD_DIST"
fi
```

### Post-Build Hook Example

```bash
#!/bin/sh
# hooks/post_build.sh

# Generate checksums
cd "$FREEBSD_DIST"
find . -type f -exec sha256sum {} \; > ../checksums.txt

# Sign binaries
for binary in bin/* sbin/*; do
    gpg --detach-sign "$binary"
done
```

## Testing & Validation

### Running Tests

```python
from modules.testing import TestRunner, VMTester
from modules.config import Config

config = Config('./freebsd_workspace', 'MyOS', '14.0-RELEASE', 'amd64')

# Run validation tests
tester = TestRunner(config)
tester.run_all_tests()

# Test in QEMU
vm_tester = VMTester(config)
vm_tester.test_in_qemu()
```

## Advanced Examples

### Example 1: Security-Hardened OS

```json
{
  "os_name": "SecureBSD",
  "kernel_options": [
    "MAC",
    "MAC_BIBA",
    "MAC_LOMAC",
    "AUDIT"
  ],
  "custom_sysctl": {
    "security.bsd.see_other_uids": "0",
    "security.bsd.unprivileged_read_msgbuf": "0",
    "kern.randompid": "1"
  }
}
```

### Example 2: Router/Firewall OS

```json
{
  "os_name": "RouterBSD",
  "kernel_options": [
    "ALTQ",
    "ALTQ_CBQ",
    "ALTQ_RED",
    "IPSEC",
    "NETGRAPH"
  ],
  "kernel_devices": [
    "pf",
    "pflog",
    "carp"
  ],
  "custom_packages": [
    "net/bird2",
    "net/frr",
    "security/strongswan"
  ]
}
```

### Example 3: Minimal Embedded OS

```json
{
  "os_name": "EmbeddedBSD",
  "src_conf_additions": [
    "WITHOUT_GAMES=yes",
    "WITHOUT_SENDMAIL=yes",
    "WITHOUT_EXAMPLES=yes",
    "WITHOUT_MAN=yes"
  ],
  "kernel_nodevices": [
    "fdc",
    "uart",
    "sound"
  ]
}
```

## Performance Optimization

### Compiler Optimizations

```json
{
  "make_conf_additions": [
    "CPUTYPE?=native",
    "WITH_CCACHE_BUILD=yes",
    "CFLAGS+=-O3 -march=native"
  ]
}
```

### Parallel Building

```bash
# Use all CPU cores
python freebsd_builder.py --all --jobs $(nproc)
```

## Troubleshooting

### Build Failures

```bash
# Clean and rebuild
python freebsd_builder.py --clean
python freebsd_builder.py --build

# Check logs
tail -f freebsd_workspace/build.log
```

### Patch Conflicts

```bash
# Review failed patches
cat freebsd_workspace/patches_applied.log

# Manually apply
cd freebsd_workspace/src
patch -p0 < ../patches/001-my-patch.patch
```

## Best Practices

1. **Version Control**: Keep your config and patches in git
2. **Incremental Builds**: Use `--build` instead of `--all` for faster iterations
3. **Test in VM**: Always test in QEMU before deploying
4. **Backup**: Use pre-build hooks to backup previous builds
5. **Documentation**: Document all customizations in patches/README.md

## Resources

- [FreeBSD Handbook](https://docs.freebsd.org/en/books/handbook/)
- [FreeBSD Kernel Configuration](https://docs.freebsd.org/en/books/handbook/kernelconfig/)
- [FreeBSD Ports](https://docs.freebsd.org/en/books/porters-handbook/)
