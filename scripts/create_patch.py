#!/usr/bin/env python3
"""Helper script to create patches from git changes"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.patches import PatchManager
from modules.config import Config

def main():
    parser = argparse.ArgumentParser(description='Create patch from git changes')
    parser.add_argument('description', help='Patch description')
    parser.add_argument('--files', nargs='+', help='Specific files to include')
    parser.add_argument('--work-dir', default='./freebsd_workspace', help='Working directory')
    
    args = parser.parse_args()
    
    config = Config(args.work_dir, "CustomBSD", "14.0-RELEASE", "amd64")
    patch_manager = PatchManager(config)
    
    patch_manager.create_patch(args.description, args.files)

if __name__ == '__main__':
    main()
