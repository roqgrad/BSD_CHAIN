# Patches Directory

Place your custom patches here. Patches will be applied in alphabetical order.

## Creating Patches

### Method 1: Using git diff
```bash
cd freebsd_workspace/src
# Make your changes
git diff > ../patches/001-my-custom-patch.patch
```

### Method 2: Using the toolchain
```python
from modules.patches import PatchManager
from modules.config import Config

config = Config("./freebsd_workspace", "MyOS", "14.0-RELEASE", "amd64")
patch_manager = PatchManager(config)
patch_manager.create_patch("my custom feature", ["path/to/file.c"])
```

## Patch Format

Patches should be in unified diff format:
```
--- a/sys/kern/kern_exec.c
+++ b/sys/kern/kern_exec.c
@@ -100,6 +100,7 @@
 #include <sys/proc.h>
+#include <sys/custom.h>
```

## Naming Convention

Use numbered prefixes for ordering:
- `001-security-hardening.patch`
- `002-custom-driver.patch`
- `003-performance-optimization.patch`

## Example Patches

### Security Hardening
```patch
--- a/sys/kern/kern_fork.c
+++ b/sys/kern/kern_fork.c
@@ -500,6 +500,8 @@
+    /* Custom security check */
+    if (security_check_fork(td) != 0)
+        return (EPERM);
```

### Custom Branding
```patch
--- a/sys/sys/param.h
+++ b/sys/sys/param.h
@@ -60,7 +60,7 @@
-#define __FreeBSD_version 1400000
+#define __FreeBSD_version 1400001
```
