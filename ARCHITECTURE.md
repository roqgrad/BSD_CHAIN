# FreeBSD Custom OS Builder - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   freebsd_builder.py                        │
│                   (Main Orchestrator)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Clone   │  │Customize │  │  Build   │
│  Module  │  │  Module  │  │  Module  │
└──────────┘  └──────────┘  └──────────┘
        │            │            │
        └────────────┼────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Patches │  │ Packages │  │   ISO    │
│  Module  │  │  Module  │  │  Module  │
└──────────┘  └──────────┘  └──────────┘
```

## Module Descriptions

### Core Modules

#### config.py
- Manages all configuration settings
- Handles JSON config file I/O
- Provides default values
- Validates configuration

#### clone.py
- Clones FreeBSD source from git
- Handles repository updates
- Manages git branches and versions

#### customize.py
- Applies OS branding
- Modifies kernel configuration
- Updates version strings
- Creates custom RC scripts
- Applies system-wide customizations

#### build.py
- Orchestrates build process
- Builds world (userland)
- Builds kernel
- Creates distribution files
- Manages build hooks

### Advanced Modules

#### patches.py
- Applies custom patches
- Creates patches from changes
- Manages patch ordering
- Logs patch application

#### packages.py
- Clones ports tree
- Builds custom packages
- Creates package manifests
- Integrates packages into OS

#### iso.py
- Creates bootable ISO images
- Generates USB memstick images
- Prepares boot structure
- Supports multiple ISO tools

#### hooks.py
- Executes pre-build hooks
- Executes post-build hooks
- Provides build environment variables
- Supports shell scripts and commands

#### testing.py
- Validates build artifacts
- Tests kernel and world
- Generates test reports
- Supports VM testing (QEMU)

## Data Flow

```
Config File (JSON)
       │
       ▼
   Config Object
       │
       ├──> Clone Module ──> FreeBSD Source
       │
       ├──> Customize Module ──> Modified Source
       │                              │
       │                              ├──> Patches
       │                              ├──> Branding
       │                              └──> Kernel Config
       │
       ├──> Build Module ──> Build Artifacts
       │                          │
       │                          ├──> World
       │                          ├──> Kernel
       │                          └──> Distribution
       │
       └──> ISO Module ──> Bootable Images
```

## Configuration Hierarchy

```
Config
├── Basic Settings
│   ├── work_dir
│   ├── os_name
│   ├── version
│   └── target_arch
│
├── Build Options
│   ├── make_jobs
│   ├── kernel_config
│   └── build_options
│
├── Customization
│   ├── kernel_options
│   ├── kernel_devices
│   ├── custom_motd
│   ├── custom_rc_conf
│   └── custom_sysctl
│
├── Packages
│   ├── enable_ports
│   ├── ports_repo
│   └── custom_packages
│
├── Patches
│   └── patch_dir
│
├── ISO Creation
│   ├── create_iso
│   ├── iso_label
│   └── iso_volume
│
└── Hooks
    ├── pre_build_hooks
    └── post_build_hooks
```

## Build Process Flow

```
1. Initialize
   └─> Load Configuration
   └─> Validate Settings

2. Clone Phase
   └─> Clone FreeBSD Source
   └─> Checkout Branch/Version

3. Customize Phase
   └─> Apply Branding
   └─> Modify Kernel Config
   └─> Apply Patches
   └─> Update System Files

4. Pre-Build Hooks
   └─> Execute Custom Scripts

5. Build Phase
   └─> Build World
   └─> Build Kernel
   └─> Create Distribution

6. Post-Build Hooks
   └─> Execute Custom Scripts

7. Package Phase (Optional)
   └─> Build Custom Packages
   └─> Create Manifest

8. ISO Phase (Optional)
   └─> Prepare ISO Structure
   └─> Create Bootable ISO

9. Testing Phase (Optional)
   └─> Validate Build
   └─> Test in VM
```

## Extension Points

### Adding New Customizations

1. Add configuration option to `Config` class
2. Implement customization in `FreeBSDCustomizer`
3. Update example config files

### Adding New Build Targets

1. Extend `FreeBSDBuilder` class
2. Add command-line argument
3. Update main orchestrator

### Adding New Hooks

1. Add hook list to `Config`
2. Implement in `HookManager`
3. Call from appropriate build phase

## File Structure

```
freebsd_builder/
├── freebsd_builder.py          # Main entry point
├── modules/
│   ├── __init__.py
│   ├── config.py               # Configuration
│   ├── clone.py                # Source cloning
│   ├── customize.py            # Customization
│   ├── build.py                # Build process
│   ├── patches.py              # Patch management
│   ├── packages.py             # Package management
│   ├── iso.py                  # ISO creation
│   ├── hooks.py                # Build hooks
│   └── testing.py              # Testing
├── patches/                    # Custom patches
├── hooks/                      # Build hooks
├── scripts/                    # Helper scripts
├── docker/                     # Docker support
└── freebsd_workspace/          # Build workspace
    ├── src/                    # FreeBSD source
    ├── obj/                    # Build objects
    ├── dist/                   # Distribution
    ├── ports/                  # Ports tree
    └── iso/                    # ISO staging
```

## Design Principles

1. **Modularity**: Each module has a single responsibility
2. **Configurability**: Everything is configurable via JSON
3. **Extensibility**: Easy to add new features
4. **Automation**: Minimal manual intervention
5. **Validation**: Built-in testing and validation
6. **Documentation**: Comprehensive documentation

## Performance Considerations

- Parallel builds using `-j` flag
- Incremental builds support
- Ccache integration
- Efficient git cloning (shallow clones)
- Optimized compiler flags

## Security Considerations

- Patch validation
- Checksum generation
- Binary signing support (via hooks)
- Secure defaults
- Audit logging
