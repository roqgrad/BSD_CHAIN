# FreeBSD Custom OS Builder

A comprehensive Python toolchain for cloning, customizing, and building your own FreeBSD-based operating system.

## Features

- Clone FreeBSD source code from official repository
- Customize OS branding and version strings
- Create custom kernel configurations
- Build complete OS distribution
- Modular architecture for easy extension

## Prerequisites

### System Requirements
- Git
- FreeBSD build tools (make, compiler toolchain)
- Python 3.7+
- Disk space: ~30GB for source + build artifacts
- RAM: 4GB minimum, 8GB+ recommended

### On FreeBSD
```bash
pkg install git python3
```

### On Linux (cross-compilation)
```bash
# Install FreeBSD toolchain for your distribution
# This varies by distro - consult FreeBSD documentation
```

## Quick Start

### 1. Clone and Build Everything
```bash
python freebsd_builder.py --all --os-name "MyOS" --version "14.0-RELEASE"
```

### 2. Step-by-Step Workflow

```bash
# Clone FreeBSD source
python freebsd_builder.py --clone --version "14.0-RELEASE"

# Apply customizations
python freebsd_builder.py --customize --os-name "MyOS"

# Build the OS
python freebsd_builder.py --build --target "amd64"
```

## Configuration

### Command Line Options

- `--all`: Run complete workflow (clone + customize + build)
- `--clone`: Clone FreeBSD source code
- `--customize`: Apply customizations
- `--build`: Build the OS
- `--clean`: Clean build artifacts
- `--version`: FreeBSD version (default: 14.0-RELEASE)
- `--os-name`: Your custom OS name (default: CustomBSD)
- `--target`: Target architecture (default: amd64)
- `--work-dir`: Working directory (default: ./freebsd_workspace)
- `--config`: Load configuration from JSON file

### Configuration File

Create a `config.json` file:

```json
{
  "work_dir": "./freebsd_workspace",
  "os_name": "MyOS",
  "version": "14.0-RELEASE",
  "target_arch": "amd64",
  "kernel_config": "GENERIC",
  "make_jobs": 8
}
```

Use it:
```bash
python freebsd_builder.py --all --config config.json
```

## Project Structure

```
freebsd_builder.py          # Main entry point
modules/
  ├── __init__.py
  ├── config.py             # Configuration management
  ├── clone.py              # Source cloning
  ├── customize.py          # OS customization
  └── build.py              # Build orchestration
freebsd_workspace/          # Created during build
  ├── src/                  # FreeBSD source code
  ├── obj/                  # Build objects
  └── dist/                 # Distribution files
```

## Customizations Applied

The toolchain automatically applies these customizations:

1. **Branding**: Replaces "FreeBSD" with your OS name
2. **Kernel Config**: Creates custom kernel configuration
3. **Version Strings**: Updates system identification
4. **RC Scripts**: Adds custom initialization scripts

## Advanced Usage

### Custom Kernel Configuration

Edit the generated kernel config:
```bash
# After running --customize
nano freebsd_workspace/src/sys/amd64/conf/MYOS
```

### Adding More Customizations

Extend `modules/customize.py`:

```python
def _add_custom_packages(self):
    """Add custom packages to base system"""
    # Your implementation
    pass
```

## Build Output

After successful build, find your OS in:
- `freebsd_workspace/dist/` - Distribution files
- `freebsd_workspace/obj/` - Build artifacts

## Creating Installation Media

```bash
# Create bootable ISO (on FreeBSD)
cd freebsd_workspace/dist
sh /usr/src/release/amd64/mkisoimages.sh -b MyOS_label MyOS.iso /path/to/dist
```

## Troubleshooting

### Build Fails
- Ensure you have enough disk space (30GB+)
- Check build logs in terminal output
- Verify FreeBSD build tools are installed

### Git Clone Fails
- Check internet connection
- Verify git is installed
- Try different branch/version

### Customization Issues
- Review `freebsd_workspace/customizations.log`
- Check file permissions
- Ensure source was cloned successfully

## Contributing

Feel free to extend this toolchain:
1. Add new customization modules
2. Support additional architectures
3. Implement ISO creation automation
4. Add testing frameworks

## Resources

- [FreeBSD Handbook](https://docs.freebsd.org/en/books/handbook/)
- [FreeBSD Source Repository](https://git.freebsd.org/src.git)
- [Building FreeBSD](https://docs.freebsd.org/en/books/handbook/cutting-edge/)

## License

This toolchain is provided as-is for educational and development purposes.
FreeBSD source code is subject to FreeBSD license terms.

## Notes

- Building FreeBSD can take 1-4 hours depending on hardware
- First build is always slower (subsequent builds are incremental)
- Cross-compilation from non-FreeBSD systems requires additional setup
- Always test in virtual machines before deploying to hardware
