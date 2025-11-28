# Quick Start Guide

Get your custom FreeBSD OS built in minutes!

## 1. Setup Environment

### On Ubuntu:
```bash
chmod +x setup_env_ubuntu.sh
./setup_env_ubuntu.sh
```

### On FreeBSD:
```bash
chmod +x setup_env_freebsd.sh
./setup_env_freebsd.sh
```

This will install:
- VS Code with extensions
- Python environment
- Build tools
- Docker
- Git configuration

## 2. Load Environment

```bash
source .env
```

This activates the Python virtual environment and sets up aliases.

## 3. Build Your OS

### Option A: Interactive Wizard
```bash
bash scripts/quick_start.sh
```

### Option B: Command Line
```bash
# Full build with ISO
python freebsd_builder.py --all \
  --os-name "MyOS" \
  --version "14.0-RELEASE" \
  --create-iso \
  --jobs 8

# Or use the alias
fbuild --all --os-name "MyOS" --create-iso
```

### Option C: Using Makefile
```bash
# Edit example_config.json first
make all CONFIG=example_config.json
```

## 4. Test Your OS

```bash
# Test in QEMU
qemu-system-x86_64 -cdrom freebsd_workspace/MyOS_14.0-RELEASE_amd64.iso -m 2048
```

## 5. Next Steps

- Read [ADVANCED_GUIDE.md](ADVANCED_GUIDE.md) for advanced features
- Check [FEATURES.md](FEATURES.md) for complete feature list
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design

## Common Commands

```bash
# Clone only
fbuild --clone --version "14.0-RELEASE"

# Customize only
fbuild --customize --os-name "MyOS"

# Build only
fbuild --build

# Create ISO
fbuild --create-iso

# Clean build
fbuild --clean

# Full workflow with monitoring
fbuild --all --monitor --os-name "MyOS"

# Security hardened build
fbuild --all --harden --os-name "SecureBSD"

# Cloud images
fbuild --all --cloud-aws --cloud-azure --cloud-gcp

# Backup current build
fbuild --backup
```

## Configuration

Create a custom config file:

```json
{
  "os_name": "MyCustomOS",
  "version": "14.0-RELEASE",
  "target_arch": "amd64",
  "make_jobs": 8,
  "create_iso": true,
  "custom_packages": ["bash", "vim", "git"],
  "kernel_options": ["ALTQ", "IPSEC"]
}
```

Use it:
```bash
fbuild --all --config my_config.json
```

## Troubleshooting

### Build fails
```bash
# Check logs
tail -f freebsd_workspace/build.log

# Clean and retry
fbuild --clean
fbuild --build
```

### Out of disk space
```bash
# Check usage
df -h

# Clean old builds
rm -rf freebsd_workspace/obj/*
```

### Git clone fails
```bash
# Use shallow clone
fbuild --clone --version "14.0-RELEASE"
```

## Tips

1. **Use ccache**: Speeds up rebuilds significantly
2. **Parallel builds**: Use `--jobs $(nproc)` for faster builds
3. **Incremental builds**: Only rebuild changed components
4. **Test in VM**: Always test before deploying to hardware
5. **Backup configs**: Keep your config files in version control

## Support

- Check documentation in `docs/` directory
- Review example configurations
- Read inline code comments
- Check GitHub issues (if applicable)

## What's Next?

- Customize kernel configuration
- Add custom patches
- Build custom packages
- Create cloud images
- Set up automated builds
- Deploy to production

Happy building! 🚀
