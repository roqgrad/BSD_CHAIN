"""Tests for configuration module"""

import pytest
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.config import Config

def test_config_creation():
    """Test basic config creation"""
    config = Config("./test_workspace", "TestOS", "14.0-RELEASE", "amd64")
    
    assert config.os_name == "TestOS"
    assert config.version == "14.0-RELEASE"
    assert config.target_arch == "amd64"
    assert config.make_jobs == 4

def test_config_paths():
    """Test config path generation"""
    config = Config("./test_workspace", "TestOS", "14.0-RELEASE", "amd64")
    
    assert config.src_dir == config.work_dir / "src"
    assert config.obj_dir == config.work_dir / "obj"
    assert config.dist_dir == config.work_dir / "dist"

def test_config_save_load(tmp_path):
    """Test config save and load"""
    config = Config("./test_workspace", "TestOS", "14.0-RELEASE", "amd64")
    config.make_jobs = 8
    
    config_file = tmp_path / "test_config.json"
    config.save_to_file(config_file)
    
    assert config_file.exists()
    
    # Load and verify
    with open(config_file, 'r') as f:
        data = json.load(f)
    
    assert data['os_name'] == "TestOS"
    assert data['make_jobs'] == 8

def test_git_branch_generation():
    """Test automatic git branch generation"""
    config = Config("./test_workspace", "TestOS", "14.0-RELEASE", "amd64")
    
    assert config.git_branch == "releng/14.0"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
