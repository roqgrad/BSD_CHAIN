#!/usr/bin/env python3
"""
FreeBSD Custom OS Builder - Main Entry Point
Orchestrates the entire FreeBSD customization workflow
"""

import argparse
import sys
from pathlib import Path
from modules.clone import FreeBSDCloner
from modules.customize import FreeBSDCustomizer
from modules.build import FreeBSDBuilder
from modules.config import Config
from modules.iso import ISOCreator
from modules.packages import PackageManager
from modules.monitoring import BuildMonitor, ProgressTracker
from modules.security import SecurityHardener, BinarySigner
from modules.backup import BackupManager
from modules.documentation import DocumentationGenerator
from modules.cloud import CloudImageGenerator

def main():
    parser = argparse.ArgumentParser(
        description='FreeBSD Custom OS Builder Toolchain',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full workflow with ISO
  python freebsd_builder.py --all --os-name "MyOS" --version "14.0-RELEASE" --create-iso
  
  # Individual steps
  python freebsd_builder.py --clone --version "14.0-RELEASE"
  python freebsd_builder.py --customize --os-name "MyOS"
  python freebsd_builder.py --build --target "amd64"
  python freebsd_builder.py --create-iso
  
  # With custom config
  python freebsd_builder.py --all --config advanced_config.json
  
  # Build release with packages
  python freebsd_builder.py --all --setup-ports --build-packages
        """
    )
    
    # Main workflow options
    parser.add_argument('--all', action='store_true', help='Run complete workflow')
    parser.add_argument('--clone', action='store_true', help='Clone FreeBSD source')
    parser.add_argument('--customize', action='store_true', help='Apply customizations')
    parser.add_argument('--build', action='store_true', help='Build the OS')
    parser.add_argument('--build-release', action='store_true', help='Build full release')
    parser.add_argument('--clean', action='store_true', help='Clean build artifacts')
    
    # ISO/Image creation
    parser.add_argument('--create-iso', action='store_true', help='Create bootable ISO')
    parser.add_argument('--create-memstick', action='store_true', help='Create USB memstick image')
    
    # Package management
    parser.add_argument('--setup-ports', action='store_true', help='Clone ports tree')
    parser.add_argument('--build-packages', action='store_true', help='Build custom packages')
    
    # Security
    parser.add_argument('--harden', action='store_true', help='Apply security hardening')
    parser.add_argument('--sign', action='store_true', help='Generate checksums and signatures')
    
    # Cloud images
    parser.add_argument('--cloud-aws', action='store_true', help='Generate AWS AMI image')
    parser.add_argument('--cloud-azure', action='store_true', help='Generate Azure VHD image')
    parser.add_argument('--cloud-gcp', action='store_true', help='Generate GCP image')
    
    # Utilities
    parser.add_argument('--backup', action='store_true', help='Backup current build')
    parser.add_argument('--generate-docs', action='store_true', help='Generate documentation')
    parser.add_argument('--monitor', action='store_true', help='Enable build monitoring')
    
    # Configuration options
    parser.add_argument('--version', default='14.0-RELEASE', help='FreeBSD version')
    parser.add_argument('--os-name', default='CustomBSD', help='Your OS name')
    parser.add_argument('--target', default='amd64', help='Target architecture (amd64, arm64, i386, riscv64)')
    parser.add_argument('--work-dir', default='./freebsd_workspace', help='Working directory')
    parser.add_argument('--config', help='Custom config file path')
    parser.add_argument('--jobs', type=int, default=4, help='Number of parallel make jobs')
    
    # Advanced options
    parser.add_argument('--cross-compile', help='Cross-compilation toolchain')
    parser.add_argument('--kernel-config', default='GENERIC', help='Base kernel config')
    parser.add_argument('--save-config', help='Save current config to file')
    
    args = parser.parse_args()
    
    # Load configuration
    config = Config(args.work_dir, args.os_name, args.version, args.target)
    config.make_jobs = args.jobs
    config.kernel_config = args.kernel_config
    
    if args.cross_compile:
        config.cross_toolchain = args.cross_compile
    
    if args.create_iso:
        config.create_iso = True
    
    if args.config:
        config.load_from_file(args.config)
    
    # Save config if requested
    if args.save_config:
        config.save_to_file(args.save_config)
        print(f"[✓] Configuration saved to {args.save_config}")
        return
    
    try:
        # Initialize monitoring
        monitor = None
        if args.monitor or args.all:
            monitor = BuildMonitor(config)
            monitor.start()
        
        # Apply security hardening if requested
        if args.harden or args.all:
            print(f"\n{'='*60}")
            print(f"[*] Applying security hardening...")
            print(f"{'='*60}")
            hardener = SecurityHardener(config)
            hardener.apply_hardening()
        
        # Execute workflow
        if args.all or args.clone:
            print(f"\n{'='*60}")
            print(f"[*] Cloning FreeBSD {args.version}...")
            print(f"{'='*60}")
            cloner = FreeBSDCloner(config)
            cloner.clone()
        
        if args.all or args.setup_ports:
            print(f"\n{'='*60}")
            print(f"[*] Setting up ports tree...")
            print(f"{'='*60}")
            pkg_manager = PackageManager(config)
            pkg_manager.setup_ports()
        
        if args.all or args.customize:
            print(f"\n{'='*60}")
            print(f"[*] Customizing to {args.os_name}...")
            print(f"{'='*60}")
            customizer = FreeBSDCustomizer(config)
            customizer.apply_customizations()
        
        if args.build_packages:
            print(f"\n{'='*60}")
            print(f"[*] Building custom packages...")
            print(f"{'='*60}")
            pkg_manager = PackageManager(config)
            pkg_manager.build_custom_packages()
            pkg_manager.create_package_manifest()
        
        if args.all or args.build:
            print(f"\n{'='*60}")
            print(f"[*] Building {args.os_name}...")
            print(f"{'='*60}")
            builder = FreeBSDBuilder(config)
            builder.build()
        
        if args.build_release:
            print(f"\n{'='*60}")
            print(f"[*] Building full release...")
            print(f"{'='*60}")
            builder = FreeBSDBuilder(config)
            builder.build_release()
        
        if args.all or args.create_iso:
            print(f"\n{'='*60}")
            print(f"[*] Creating ISO image...")
            print(f"{'='*60}")
            iso_creator = ISOCreator(config)
            iso_creator.create_iso()
        
        if args.create_memstick:
            print(f"\n{'='*60}")
            print(f"[*] Creating memstick image...")
            print(f"{'='*60}")
            iso_creator = ISOCreator(config)
            iso_creator.create_memstick_image()
        
        if args.clean:
            print(f"\n{'='*60}")
            print(f"[*] Cleaning build artifacts...")
            print(f"{'='*60}")
            builder = FreeBSDBuilder(config)
            builder.clean()
        
        # Generate checksums and signatures
        if args.sign:
            print(f"\n{'='*60}")
            print(f"[*] Generating checksums...")
            print(f"{'='*60}")
            signer = BinarySigner(config)
            signer.generate_checksums()
        
        # Cloud images
        if args.cloud_aws or args.cloud_azure or args.cloud_gcp:
            cloud_gen = CloudImageGenerator(config)
            
            if args.cloud_aws:
                print(f"\n{'='*60}")
                print(f"[*] Generating AWS AMI image...")
                print(f"{'='*60}")
                cloud_gen.generate_aws_ami()
            
            if args.cloud_azure:
                print(f"\n{'='*60}")
                print(f"[*] Generating Azure VHD image...")
                print(f"{'='*60}")
                cloud_gen.generate_azure_vhd()
            
            if args.cloud_gcp:
                print(f"\n{'='*60}")
                print(f"[*] Generating GCP image...")
                print(f"{'='*60}")
                cloud_gen.generate_gcp_image()
        
        # Backup
        if args.backup:
            print(f"\n{'='*60}")
            print(f"[*] Creating backup...")
            print(f"{'='*60}")
            backup_mgr = BackupManager(config)
            backup_mgr.backup_build()
        
        # Generate documentation
        if args.generate_docs or args.all:
            print(f"\n{'='*60}")
            print(f"[*] Generating documentation...")
            print(f"{'='*60}")
            doc_gen = DocumentationGenerator(config)
            doc_gen.generate_all()
        
        # Finalize monitoring
        if monitor:
            monitor.checkpoint("Build Complete")
            monitor.generate_report()
        
        print(f"\n{'='*60}")
        print(f"[✓] Success! Your custom OS is ready.")
        print(f"{'='*60}")
        print(f"\nWorkspace: {config.work_dir}")
        print(f"Distribution: {config.dist_dir}")
        if config.create_iso:
            print(f"ISO files: {config.work_dir}")
        
    except KeyboardInterrupt:
        print(f"\n[!] Build interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n[✗] Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
